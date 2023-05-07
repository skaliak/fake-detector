from __future__ import annotations
import praw, logging, os, datetime

# Reddit API access

class RedditAccess:
    def __init__(self, timeframe: str = 'week'):
        logging.info(f"RedditAccess.__init__() ... timeframe = {timeframe}")
        self._timeframe = timeframe
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")
        logging.info(f"user agent for reddit: {user_agent}")
        if client_id is None:
            # use praw.ini
            self.reddit = praw.Reddit("bot1")
        else:
            self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        logging.info("Logged in as {}".format(self.reddit.user.me()))

    def get_reddit(self) -> praw.Reddit:
        return self.reddit
    
    # returns true if a user exists, otherwise false (catches 404 errors)
    def user_exists(self, username: str) -> bool:
        try:
            self.reddit.redditor(username).id
            return True
        except Exception as e:
            if 'NotFound' in str(type(e)):
                return False
            else:
                raise e

    def get_user_details(self, username:str, include_trophies:bool = False) -> dict:
        if not self.user_exists(username):
            return {'error': 'user does not exist'}
        user = self.reddit.redditor(username)
        bio = user.subreddit.public_description
        week_subs = list(self.get_subreddits_posted_in_by_user(username))
        month_subs = list(self.get_subreddits_posted_in_by_user(username, 'month'))
        week_comments = list(self.get_subreddits_commented_in_by_user(username))
        created = user.created_utc
        trophies = [t.name for t in user.trophies()] if include_trophies else []
        return {
            'total_karma': user.link_karma + user.comment_karma,
            'bio': bio,
            'week_subs': week_subs,
            'month_subs': month_subs,
            'week_comments': week_comments, # TODO: add month comments
            'created': datetime.datetime.fromtimestamp(created).isoformat(),
            'trophies': trophies
        }

    # Returns a set of subreddit names that the user has posted in recently
    def get_subreddits_posted_in_by_user(self, username: str, time: str = 'week') -> set[str]:
        submissions = self.reddit.redditor(username).submissions.top(time_filter=time)
        return {s.subreddit.display_name for s in submissions}

    # Returns a set of subreddit names that the user has commented in recently
    def get_subreddits_commented_in_by_user(self, username: str, time: str = 'week') -> set[str]:
        comments = self.reddit.redditor(username).comments.top(time_filter=time)
        return {c.subreddit.display_name for c in comments}

    # returns a list of subreddits matching the pattern 'r4r'
    def get_r4r_subreddits(self) -> list:
        return [s.display_name for s in self.reddit.subreddits.search("r4r")]

def main():
    print("reddit_access.py")
    reddit = RedditAccess()
    # print(reddit.get_subreddits_posted_in_by_user("moregooderer1"))
    print(reddit.get_r4r_subreddits())

if __name__ == "__main__":
    main()