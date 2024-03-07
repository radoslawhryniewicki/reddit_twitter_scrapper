import logging
from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError, Page

from .base import BaseScrapper
from scrappers.exceptions import CommunityNotFoundExc

REDDIT_POSTS_AMOUNT_TO_SCRAP = 5

class RedditScrapper(BaseScrapper):
    def __init__(self, subreddit: str):
        self._subreddit = subreddit
        self._url = f"https://www.reddit.com/r/{self._subreddit}/new/?feedViewType=classicView"

    def _check_community_exist(self, page: Page):
        if page.get_by_text('Community not found').is_visible():
            raise CommunityNotFoundExc(self._subreddit)

    @staticmethod
    def _reject_cookies(page: Page) -> None:
        try:
            page.click("#reject-nonessential-cookies-button", timeout=2_000)
        except PWTimeoutError:
            print("No cookie window appeared.")

    @staticmethod
    def _trim_posts(articles: list[Tag]) -> list[Tag]:
        excess_posts = len(articles) - REDDIT_POSTS_AMOUNT_TO_SCRAP
        return articles[:-excess_posts]

    @staticmethod
    def _is_pinned_post(post: Tag):
        svg_class_value = post.find('svg', {'aria-label': 'Sticked post'}).get('class')
        return 'hidden' not in svg_class_value

    def _collect_all_subreddit_posts(self, page: Page) -> list[Tag]:
        posts = []
        while len(posts) < REDDIT_POSTS_AMOUNT_TO_SCRAP:
            content = page.locator("#main-content").inner_html()
            soup = BeautifulSoup(content, 'html.parser')
            posts = soup.find_all('article')
            for index, post in enumerate(posts):
                if self._is_pinned_post(post):
                    posts.pop(index)

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        if len(posts) > REDDIT_POSTS_AMOUNT_TO_SCRAP:
            return self._trim_posts(posts)
        return posts

    @staticmethod
    def _get_post_content(post_id: str, post_title: str, page: Page):
        content_page = page.locator(f'#{post_id}', has_text=post_title)
        # We also have to filter by post_title cause post_id
        # on reddit DOM can be located in more than one place unfortunately
        content_page.click()
        try:
            content = page.locator(f'#{post_id}-post-rtjson-content').inner_text(timeout=2_000)
            return content.replace('\n', ' ')
        except PWTimeoutError:
            return 'Post has only attached photo or video. No text content'
        finally:
            page.go_back()
            page.wait_for_timeout(500)
            # reddit has built-in protection against constant access to subpages,
            # so we need to wait a bit to enter and do not get an error.

    def _extract_post_details(self, post, page):
        reddit_post = post.find('shreddit-post')
        post_content = self._get_post_content(reddit_post['id'], reddit_post['post-title'], page)
        return {
            "subreddit_name": reddit_post['subreddit-prefixed-name'],
            "title": reddit_post['post-title'],
            "content": post_content,
            "comment_count": int(reddit_post['comment-count']),
            "rating": int(reddit_post['score']),
        }

    def scrap(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self._url)
            logging.info(f"Reddit (#{self._subreddit}) scrapping started.")
            self._check_community_exist(page)
            self._reject_cookies(page)
            posts = self._collect_all_subreddit_posts(page)
            posts_details = [self._extract_post_details(post, page) for post in posts]
            logging.info("Get all posts details. Scrapping ended.")
            browser.close()
            return posts_details
