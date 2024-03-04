from pydantic import BaseModel


class TweetDetails(BaseModel):
    hashtag: str
    content: str
