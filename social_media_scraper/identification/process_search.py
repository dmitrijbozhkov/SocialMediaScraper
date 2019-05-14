""" Search prcessing functionality """
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait
from social_media_scraper.identification.external_resources import Browsers
from social_media_scraper.twitter.identity_search.searcher import TwitterSearcher
from social_media_scraper.linked_in.identity_search.searcher import LinkedInSearcher
from social_media_scraper.xing.identity_search.searcher import XingSearcher

MatchLinks = namedtuple("MatchLinks", ["LinkedInLink", "XingLink", "TwitterLink"])

def identity_matcher(browsers: Browsers):
    """
    Match identities in LinkedIn and Xing
    :param browsers Browsers: Browsers for LinkedIn and Xing
    """
    executor = ThreadPoolExecutor(3)
    result: MatchLinks = None
    twitter_searcher = TwitterSearcher(browsers.Twitter)
    linked_in_searcher = LinkedInSearcher(browsers.LinkedIn)
    xing_searcher = XingSearcher(browsers.Xing)
    try:
        while True:
            search_keywords = yield result
            linked_in_fututre = executor.submit(
                linked_in_searcher.search_account,
                search_keywords)
            xing_future = executor.submit(
                xing_searcher.search_account,
                search_keywords)
            twitter_future = executor.submit(
                twitter_searcher.search_account,
                search_keywords)
            wait([linked_in_fututre, xing_future, twitter_future])
            linked_in_results = linked_in_fututre.result()
            xing_results = xing_future.result()
            twitter_result = twitter_future.result()
            result = MatchLinks(linked_in_results,
                                xing_results, twitter_result)
    except GeneratorExit:
        browsers.LinkedIn.quit()
        browsers.Xing.quit()
        browsers.Twitter.quit()
