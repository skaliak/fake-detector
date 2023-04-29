import reddit_access, data_layer

class FakeDetector:
    def __init__(self, data: data_layer.DataAccessInterface,threshold: int = 1) -> None:
        self.reddit = reddit_access.RedditAccess()
        self._threshold = threshold
        self._data = data

    # returns true if a user is a fake, false otherwise
    def is_fake(self, username: str) -> bool:
        # get the subreddits the user has posted in
        subreddits = self.reddit.get_subreddits_posted_in_by_user(username)
        # get the subreddits that are r4r subreddits
        r4r_subreddits = self._data.get_r4r_subreddits()
        # if the intersection of the two sets is greater than threshold, return true
        return len(subreddits.intersection(r4r_subreddits)) > self._threshold