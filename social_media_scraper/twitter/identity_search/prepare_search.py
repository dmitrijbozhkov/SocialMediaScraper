""" Operations, performed in order to get search results from Twitter search """
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.identification.common_scripts import build_script
from social_media_scraper.twitter.page_elements import SEARCH_RESULT_LINKS, EMPTY_RESULTS

SEARCH_LINK = URL("https://twitter.com/search")

def make_twitter_link(keywords: str) -> str:
    """
    Prepares twitter search parameters
    :param keywords str: String of keywords to pass into search field
    :return: Twitter search link
    """
    return str(SEARCH_LINK.update_query({"q": keywords, "f": "users"}))

def make_twitter_script():
    """Make twitter script"""
    return build_script(SEARCH_RESULT_LINKS)

def twitter_wait(driver: Firefox):
    """
    Waits for results to be present
    :param driver Firefox: Driver to wait on
    """
    wait = WebDriverWait(driver, 600)
    wait.until(lambda x: \
        EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT_LINKS)) or \
        EC.presence_of_element_located((By.CSS_SELECTOR, EMPTY_RESULTS)))

def twitter_account_wait(driver: Firefox):
    """
    Waits when LinkedIn account will be chosen
    :param driver Firefox: Firefox driver
    """
    return (not driver.current_url.startswith(str(SEARCH_LINK))) and driver.current_url.startswith("https://twitter.com/")
