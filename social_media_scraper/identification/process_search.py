""" Search prcessing functionality """
from functools import partial
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, wait
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from social_media_scraper.identification.external_resources import Browsers
from social_media_scraper.identification.common_scripts import NOTHING_CHOSEN_CLASS
from social_media_scraper.twitter.identity_search.prepare_search import (make_twitter_link,
                                                                         make_twitter_script,
                                                                         twitter_wait,
                                                                         twitter_account_wait)
from social_media_scraper.linked_in.identity_search.prepare_search import (make_linked_in_link,
                                                                           make_linked_in_script,
                                                                           linked_in_wait,
                                                                           linked_in_account_wait)
from social_media_scraper.xing.identity_search.prepare_search import (make_xing_link,
                                                                      make_xing_script,
                                                                      xing_wait,
                                                                      xing_account_wait)
from social_media_scraper.identification.common_scripts import SCRIPT_FUNCTIONS

MatchLinks = namedtuple("MatchLinks", ["LinkedInLink", "XingLink", "TwitterLink"])

def link_changed_wait(first_link: str, driver: Firefox):
    """
    Waiter for any link change
    """
    return first_link != driver.current_url

def wait_no_result(driver: Firefox):
    """
    Waits for an element to have a class, which states, that no element was chosen
    """
    return driver.find_element_by_css_selector(NOTHING_CHOSEN_CLASS)

def search_social_media(driver: Firefox, link: str, capture_script: str, waiting_func=None, link_chosen_wait=None) -> str:
    """
    Looks up result of the query and returns first link or chosen link if there is more than one
    :param driver Firefox: Firefox driver
    :param link str: Search link
    :param capture_script str: Script, that will get link from first result or let user choose one
    :param waiting_func Callable: Function, that waits for results to be loaded, takes driver instance as parameter
    :param link_chosen_wait Callable: Function, that waits untill user chooses appropriate account
    :return: Returns chosen account link
    """
    driver.get(link)
    if waiting_func:
        waiting_func(driver)
    result = driver.execute_script(capture_script)
    if result == 0:
        return ""
    if isinstance(result, str):
        return result
    waiter = WebDriverWait(driver, 600)
    if link_chosen_wait:
        waiter.until(lambda d: link_chosen_wait(d) or wait_no_result(d))
    else:
        waiter.until(partial(link_changed_wait, driver.current_url))
    driver.execute_script(SCRIPT_FUNCTIONS + "setDone();")
    if driver.find_element_by_css_selector(NOTHING_CHOSEN_CLASS):
        return ""
    return driver.current_url

def identity_matcher(browsers: Browsers):
    """
    Match identities in LinkedIn and Xing
    :param browsers Browsers: Browsers for LinkedIn and Xing
    """
    executor = ThreadPoolExecutor(3)
    result: MatchLinks = None
    twitter_script = make_twitter_script()
    linked_in_script = make_linked_in_script()
    xing_script = make_xing_script()
    try:
        while True:
            search_keywords = yield result
            search_keywords = " ".join(search_keywords)
            twitter_link = make_twitter_link(search_keywords)
            linked_in_link = make_linked_in_link(search_keywords)
            xing_link = make_xing_link(search_keywords)
            linked_in_fututre = executor.submit(
                search_social_media,
                browsers.LinkedIn,
                linked_in_link,
                linked_in_script,
                linked_in_wait,
                linked_in_account_wait)
            xing_future = executor.submit(
                search_social_media,
                browsers.Xing,
                xing_link,
                xing_script,
                xing_wait,
                xing_account_wait)
            twitter_future = executor.submit(
                search_social_media,
                browsers.Twitter,
                twitter_link,
                twitter_script,
                twitter_wait,
                twitter_account_wait)
            wait([linked_in_fututre, xing_future, twitter_future])
            linked_in_results = linked_in_fututre.result()
            xing_results = xing_future.result()
            twitter_result = twitter_future.result()
            result = MatchLinks(linked_in_results, xing_results, twitter_result)
    except GeneratorExit:
        browsers.LinkedIn.quit()
        browsers.Xing.quit()
        browsers.Twitter.quit()
