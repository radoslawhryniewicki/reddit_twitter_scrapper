import pytest

from reddit_twitter_scrapper.exceptions import CommunityNotFoundExc
from reddit_twitter_scrapper.script import scrape_subreddit

url = f"https://www.reddit.com/r/discordapp/new/?feedViewType=classicView"


def test_raise_exc_when_no_subreddit_found():

    with pytest.raises(CommunityNotFoundExc):
        scrape_subreddit('SomeInvalidSubredditTag')