from __future__ import annotations
import praw, logging, os

# Reddit API access

class RedditAccess:
    def __init__(self, timeframe: str = 'week'):
        logging.info(f"RedditAccess.__init__() ... timeframe = {timeframe}")
        self._timeframe = timeframe
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")
        logging.info(f"user agent for reddit: {user_agent}")
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        logging.info("Logged in as {}".format(self.reddit.user.me()))

    def get_reddit(self) -> praw.Reddit:
        return self.reddit
    
    def get_user_details(self, username:str) -> dict:
        user = self.reddit.redditor(username)
        bio = user.subreddit.public_description
        subs = list(self.get_subreddits_posted_in_by_user(username))
        created = user.created_utc
        trophies = [t.name for t in user.trophies()]
        return {
            'bio': bio,
            'subs': subs,
            'created': created,
            'trophies': trophies
        }

    # Returns a set of subreddit names that the user has posted in recently
    def get_subreddits_posted_in_by_user(self, username: str, time: str = 'week') -> set[str]:
        submissions = self.reddit.redditor(username).submissions.top(time_filter=time)
        return {s.subreddit.display_name for s in submissions}

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