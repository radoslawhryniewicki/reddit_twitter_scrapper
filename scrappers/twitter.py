import time

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError, Page

from reddit_twitter_scrapper.scrappers.base import BaseScrapper
from reddit_twitter_scrapper.xpaths import TwitterXPathEnum

PROFILE_TWEETS_AMOUNT_TO_SCRAP = 5
HASHTAG_TWEETS_AMOUNT_TO_SCRAP = 20
URL = "https://www.twitter.com"
class TwitterScrapper(BaseScrapper):
    def __init__(self, profile_name: str, hashtag: str):
        self._profile_name = profile_name
        self._hashtag = hashtag

    def login(self, page: Page):
        page.locator(TwitterXPathEnum.LOGIN_BTN.value).click()
        page.locator(TwitterXPathEnum.LOGIN_INPUT.value).fill('test.scrap.user@proton.me')
        page.locator(TwitterXPathEnum.LOGIN_FORWARD_BTN.value).click()
        page.locator(TwitterXPathEnum.USERNAME_INPUT.value).fill('JohnDoe1419566')
        page.locator(TwitterXPathEnum.USERNAME_FORWARD_BTN.value).click()
        page.locator(TwitterXPathEnum.PASSWORD_INPUT.value).fill('TestScrapping123')
        page.locator(TwitterXPathEnum.PASSWORD_FORWARD_BTN.value).click()

    def scrap(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(URL)

            self.login(page)
            page.locator(TwitterXPathEnum.SEARCH_BAR.value).fill(self._hashtag)
            page.keyboard.press('Enter')
            tweets = []

            while True:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                articles = page.query_selector_all('article')
                for article in articles:
                    tweets.append(article)
                if len(tweets) >= 20:
                    break
            print(f"LEN: {len(tweets)}")
            for t in tweets:
                print(t.text_content() + '\n')