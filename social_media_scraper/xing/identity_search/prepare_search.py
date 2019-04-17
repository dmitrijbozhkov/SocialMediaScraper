""" Operations, performed in order to get search results from Xing search """
from typing import List
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.identification.common_scripts import build_script
from social_media_scraper.xing.page_elements import SEARCH_RESULT_LINKS, NO_RESULTS_CONTAINER

SEARCH_LINK = URL("https://www.xing.com/search/members")
NO_MEMBERS_TEXT = "No members found"

def make_xing_link(keywords: str) -> str:
    """
    Prepares LinkedIn search parameters
    :param keywords str: String of keywords to pass into search field
    :return: Xing search link
    """
    return str(SEARCH_LINK.update_query({"keywords": keywords}))

def make_xing_script():
    """Make LinkedIn script"""
    return build_script(SEARCH_RESULT_LINKS)

def xing_wait(driver: Firefox):
    """
    Waits for results to be present
    :param driver Firefox: Driver to wait on
    """
    wait = WebDriverWait(driver, 600)
    wait.until(lambda x: \
        EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT_LINKS)) or \
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, NO_RESULTS_CONTAINER), NO_MEMBERS_TEXT))
