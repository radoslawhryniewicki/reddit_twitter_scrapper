from playwright.sync_api import sync_playwright
import os
from models.tweeter import TweetDetails
from db.mongo import get_database, save_to_db
from scrappers.reddit import RedditScrapper
from enums.xpaths import TwitterXPathEnum


os.environ.get('twitter_mail')
os.environ.get('twitter_username')
os.environ.get('twitter_password')
# def scrape_twitter(hashtag: str):
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         url = f"https://www.twitter.com"
#         page.goto(url)
#
#         page.locator(TwitterXPathEnum.LOGIN_BTN.value).click()
#         page.locator(TwitterXPathEnum.LOGIN_INPUT.value).fill(os.environ.get('twitter_mail'))
#         page.locator(TwitterXPathEnum.LOGIN_FORWARD_BTN.value).click()
#         page.locator(TwitterXPathEnum.USERNAME_INPUT.value).fill(os.environ.get('twitter_username'))
#         page.locator(TwitterXPathEnum.USERNAME_FORWARD_BTN.value).click()
#         page.locator(TwitterXPathEnum.PASSWORD_INPUT.value).fill(os.environ.get('twitter_password'))
#         page.locator(TwitterXPathEnum.PASSWORD_FORWARD_BTN.value).click()
#
#         page.locator(TwitterXPathEnum.SEARCH_BAR.value).fill(hashtag)
#         page.keyboard.press('Enter')
#
#         tweets = []
#         while True:
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             articles = page.query_selector_all('article')
#             for article in articles:
#                 tweets.append(article)
#             if len(tweets) >= 20:
#                 break
#
#         excess_tweets = len(tweets) - TWITTER_TWEETS_AMOUNT
#         tweets = tweets[:-excess_tweets]
#         return [TweetDetails(hashtag=hashtag, content=tweet.text_content()) for tweet in tweets]

        # try:
        #     page.get_by_test_id('emptyState').click()
        # except PWError:
        #     raise AccountDoesntExistExc(hashtag)
        # articles = []



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-subreddit",
                        help='Enter first subreddit tag to scrap. Default value set as "discordapp"',
                        default='discordapp')
    parser.add_argument("--second-subreddit",
                        help='Enter second subreddit tag to scrap. Default value set as "Polska"',
                        default='Polska')
    parser.add_argument("--twitter-hashtag",
                        help='Enter X (twitter) hashtag to scrap. Default value set as "#SpaceX"',
                        default='#SpaceX')
    parser.add_argument("--twitter-profile",
                        help='Enter X (twitter) profile to scrap. Default value set as "ElonMusk"',
                        default='ElonMusk')
    args = parser.parse_args()

    db_name = get_database()

    subreddits = [args.first_subreddit, args.second_subreddit]
    for subreddit in subreddits:
        reddit_scrapper = RedditScrapper(subreddit=subreddit)
        reddit_posts = reddit_scrapper.scrap()
        save_to_db(reddit_posts, db_name, 'reddit')

    # twitter_scrapper = TwitterScrapper(profile_name=args.twitter_profile, hashtag=args.twitter_hashtag)
    # twitter_posts_details = twitter_scrapper.scrap()
    # twitter_posts = [dict(post_detail) for post_detail in twitter_posts_details]
    # save_to_db(twitter_posts, db_name, 'twitter')