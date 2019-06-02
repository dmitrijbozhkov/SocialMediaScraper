""" External resourses management (browser drivers and files) """
from abc import ABC, abstractmethod
from typing import List
from social_media_scraper.identification.common_scripts import SCRIPT_FUNCTIONS
from social_media_scraper.identification.common_scripts import NOTHING_CHOSEN_CLASS

class Searcher(ABC):
    """ Base class for account searchers to implement """

    def __init__(self, driver, stop_script):
        self.driver = driver
        self.stop_script = stop_script

    @abstractmethod
    def wait_user_choice(self):
        """ Wait untill user chooses appropriate account or chooses no account """
        raise NotImplementedError

    @abstractmethod
    def wait_page(self):
        """ Wait for page to be ready """
        raise NotImplementedError

    @abstractmethod
    def make_link(self, keywords: List[str]):
        """ Create link with search parameters """
        raise NotImplementedError

    def join_space_skip(self, items: List[str]):
        """ Join strings by space and skip empty values """
        temp = ""
        for i in items:
            if i:
                temp += i + " "
        return temp[:-1]

    def search_account(self, keywords: List[str]):
        """
        Looks up result of the query and returns first link or chosen link if there is more than one
        :param keywords List: list of keywords to pass to search
        """
        link = self.make_link(keywords)
        self.driver.get(link)
        self.wait_page()
        result = self.driver.execute_script(self.stop_script)
        if result == 0:
            return ""
        if isinstance(result, str):
            return result
        self.wait_user_choice()
        self.driver.execute_script(SCRIPT_FUNCTIONS + "setDone();")
        if self.driver.find_elements_by_css_selector(NOTHING_CHOSEN_CLASS):
            return ""
        return self.driver.current_url
