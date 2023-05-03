

class MockFakeDetector:
    __fakes = ["vrweensy", "DeepFuckingValue", "henrypdx"]
    
    def __init__(self) -> None:
        pass

    def is_fake(self, username: str) -> bool:
        return username in self.__fakes