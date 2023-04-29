import reddit_access

class FakeDetector:
    def __init__(self) -> None:
        self.reddit = reddit_access.RedditAccess()

    