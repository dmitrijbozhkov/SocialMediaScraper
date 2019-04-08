""" Search prcessing functionality """
from typing import List
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait
from social_media_scraper.identification.external_resources import Browsers
from social_media_scraper.linked_in.identity_search.search_steps import search_linked_in, LinkedInAccountData
from social_media_scraper.xing.identity_search.search_steps import search_xing, XingAccountData

class MatchedLinks(object):
    """ Results of account search """
    def __init__(self):
        self.linked_in = None
        self.xing = None

def match_results(linked_in_results: List[LinkedInAccountData], xing_results: List[XingAccountData]) -> MatchedLinks:
    """
    Match results from both social media platforms
    :param linked_in_results List[LinkedInAccountData]: Results from LinkedIn search
    :param xing_results List[XingAccountData]: Results from Xing search
    :return: MatchedLinks instance
    """
    matches = MatchedLinks()
    if linked_in_results:
        matches.linked_in = linked_in_results[0].link
    if xing_results:
        matches.xing = xing_results[0].link
    return matches

MatchLinks = namedtuple("MatchLinks", ["LinkedInLink", "XingLink"])

def identity_matcher(browsers: Browsers):
    """
    Match identities in LinkedIn and Xing
    :param browsers Browsers: Browsers for LinkedIn and Xing
    """
    executor = ThreadPoolExecutor(2)
    result: MatchLinks = None
    try:
        while True:
            search_keywords = yield result
            search_keywords = " ".join(search_keywords)
            linked_in_fututre = executor.submit(search_linked_in, browsers.LinkedIn, search_keywords)
            xing_future = executor.submit(search_xing, browsers.Xing, search_keywords)
            wait([linked_in_fututre, xing_future])
            linked_in_results = linked_in_fututre.result()
            xing_results = xing_future.result()
            result = match_results(linked_in_results, xing_results)
    except GeneratorExit:
        browsers.LinkedIn.quit()
        browsers.Xing.quit()
