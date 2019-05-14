""" Operations, performed in order to get search results from LinkedIn search """
from typing import List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.identification.common_scripts import build_script, NOTHING_CHOSEN_CLASS
from social_media_scraper.linked_in.page_elements import SEARCH_RESULT_LINKS, EMPTY_RESULTS
from social_media_scraper.identification.external_resources import Searcher

SEARCH_LINK = URL("https://www.linkedin.com/search/results/people/")
LINKED_IN_STARTS_LINK = "https://www.linkedin.com/in/"


class LinkedInSearcher(Searcher):
    """ Searcher implementation for LinkedIn """

    def __init__(self, driver):
        super().__init__(driver, build_script(SEARCH_RESULT_LINKS))

    def wait_user_choice(self):
        """ Wait untill user chooses appropriate account or chooses no account """
        wait = WebDriverWait(self.driver, 600)
        wait.until(lambda d: \
            d.current_url.startswith(LINKED_IN_STARTS_LINK) or \
            d.find_element_by_css_selector(NOTHING_CHOSEN_CLASS))

    def wait_page(self):
        """ Wait for page to be ready """
        wait = WebDriverWait(self.driver, 600)
        wait.until(lambda d: \
            EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT_LINKS)) or \
            EC.presence_of_element_located((By.CSS_SELECTOR, EMPTY_RESULTS)))

    def make_link(self, keywords: List[str]):
        """ Create twitter LinkedIn link """
        keyword_string = self.join_space_skip(keywords)
        return str(SEARCH_LINK.update_query({"keywords": keyword_string}))
