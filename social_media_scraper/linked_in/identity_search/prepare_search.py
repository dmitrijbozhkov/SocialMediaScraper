""" Operations, performed in order to get search results from LinkedIn search """
from typing import Tuple
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.identification.common_scripts import build_script
from social_media_scraper.linked_in.page_elements import SEARCH_RESULT_LINKS, EMPTY_RESULTS

SEARCH_LINK = URL("https://www.linkedin.com/search/results/people/")

def make_linked_in_link(keywords: str) -> str:
    """
    Prepares LinkedIn search parameters
    :param keywords str: String of keywords to pass into search field
    :return: LinkedIn search link
    """
    return str(SEARCH_LINK.update_query({"keywords": keywords}))

def make_linked_in_script():
    """Make LinkedIn script"""
    return build_script(SEARCH_RESULT_LINKS)

def linked_in_wait(driver: Firefox):
    """
    Waits for results to be present
    :param driver Firefox: Driver to wait on
    """
    wait = WebDriverWait(driver, 600)
    wait.until(lambda x: \
        EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT_LINKS)) or \
        EC.presence_of_element_located((By.CSS_SELECTOR, EMPTY_RESULTS)))
