from pydantic import BaseModel


class RedditPostDetails(BaseModel):
    subreddit_name: str
    title: str
    content: str
    comment_count: int
    rating: int
