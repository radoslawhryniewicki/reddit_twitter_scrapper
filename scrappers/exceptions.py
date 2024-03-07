class CommunityNotFoundExc(Exception):
    def __init__(self, subreddit: str):
        self.message = f"Community with given subreddit tag ({subreddit}) doesn't exist"
        super().__init__(self.message)

class AccountDoesntExistExc(Exception):
    def __init__(self, hashtag: str):
        self.message = f"Hashtag ({hashtag}) doesn't exist"
        super().__init__(self.message)