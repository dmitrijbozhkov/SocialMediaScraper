""" Search prcessing functionality """
import logging
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait
from social_media_scraper.external_resources import Browsers
from social_media_scraper.twitter.identity_search.searcher import TwitterSearcher
from social_media_scraper.linked_in.identity_search.searcher import LinkedInSearcher
from social_media_scraper.xing.identity_search.searcher import XingSearcher

def identity_matcher(browsers: Browsers, executor: ThreadPoolExecutor):
    """
    Match identities in LinkedIn and Xing
    :param browsers Browsers: Browsers for LinkedIn and Xing
    """
    result = None
    twitter_searcher = TwitterSearcher(browsers.Twitter)
    linked_in_searcher = LinkedInSearcher(browsers.LinkedIn)
    xing_searcher = XingSearcher(browsers.Xing)
    while True:
        search_keywords = yield result
        twitter_future = executor.submit(
            twitter_searcher.search_account,
            search_keywords)
        linked_in_fututre = executor.submit(
            linked_in_searcher.search_account,
            search_keywords)
        xing_future = executor.submit(
            xing_searcher.search_account,
            search_keywords)
        wait([twitter_future, linked_in_fututre, xing_future])
        result = [
            search_keywords[0],
            twitter_future.result(),
            linked_in_fututre.result(),
            xing_future.result()]
        logging.info(
            "Found accounts for user %s: twitter %s linkedIn %s xing %s", *result)
