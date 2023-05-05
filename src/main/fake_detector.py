from __future__ import annotations
import logging
if __name__ == "__main__":
    import reddit_access, data_layer
else:
    from . import reddit_access, data_layer

class FakeDetector:
    def __init__(self, data: data_layer.DataAccessInterface,threshold: int = 1) -> None:
        logging.info(f"FakeDetector.__init__() ... threshold = {threshold}")
        self.reddit = reddit_access.RedditAccess()
        self._threshold = threshold
        self._data = data

    # returns true if a user is a fake, false otherwise
    def is_fake(self, username: str) -> bool:
        logging.info("FakeDetector.is_fake({})".format(username))
        # get the subreddits the user has posted in
        subreddits = self.reddit.get_subreddits_posted_in_by_user(username)
        if len(subreddits) == 0:
            logging.warning("no subreddits (or posts) found for user {} during specified timeframe".format(username))
            return False
        # get the subreddits that are r4r subreddits
        r4r_subreddits = self._data.get_r4r_subreddit_names()
        if len(r4r_subreddits) == 0:
            logging.warning("no r4r subreddits found")
            return False
        # if the intersection of the two sets is greater than threshold, return true
        result = len(subreddits.intersection(r4r_subreddits)) > self._threshold
        logging.info("FakeDetector.is_fake({}) = {}".format(username, result))
        return result
    
    # return r4r subreddits from data layer for testing
    def get_r4r_subreddits(self) -> list[str]:
        return self._data.get_r4r_subreddit_names()
    
    def get_user_bio(self, username: str) -> str:
        return self.reddit.get_user_bio(username)
    

def prompt_loop(detector: FakeDetector):
    while True:
        username = input("Enter username: ")
        if username == "":
            break
        print(detector.is_fake(username))

def main():
    logging.basicConfig(level=logging.DEBUG, filename='fakedetect_console.log', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    detector = FakeDetector(data_layer.HardCodedDataAccess())
    print("fake detector console")
    prompt_loop(detector)
    
if __name__ == "__main__":
    main()