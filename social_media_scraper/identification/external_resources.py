""" External resourses management (browser drivers and files) """
import csv
import time
import random
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Generator, List
from datetime import datetime
from selenium.webdriver import Firefox, FirefoxProfile, FirefoxOptions
from social_media_scraper.login import social_media_logins, set_login_data
from social_media_scraper.identification.common_scripts import SCRIPT_FUNCTIONS
from social_media_scraper.identification.common_scripts import NOTHING_CHOSEN_CLASS

Browsers = namedtuple("Browsers", ["LinkedIn", "Xing", "Twitter"])

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

def read_csv(file_name: str, header=False):
    """
    Reads csv row by row and skips first one
    :param file_name str: File path to read
    :param header bool: Skips header if passed True
    """
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        if header:
            next(reader)
        for row in reader:
            yield row

def write_csv(file_name: str, header=None):
    """
    Writes into csv each row
    :param file_name str: File path to write into
    :param header list: Header row
    """
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if header:
            writer.writerow(header)
        while True:
            next_row = yield
            writer.writerow(next_row)

def throttle_emissions(generator: Generator, lower_limit: int, upper_limit: int):
    """
    Passes emissions into generator in random intervals
    :param generator Generator: Generator, which emissions should be throttled (should handle infinite emissions)
    :param lower_limit int: Lower limit for throttle interval
    :param upper_limit int: Upper limit for throttle interval
    """
    next(generator)
    result = None
    current_emission = datetime.now()
    try:
        while True:
            emission = yield result
            interval = random.uniform(lower_limit, upper_limit)
            working_time = (datetime.now() - current_emission).total_seconds()
            if working_time < interval:
                time.sleep(interval - working_time)
            current_emission = datetime.now()
            result = generator.send(emission)
    except GeneratorExit:
        generator.close()
    except Exception as ex:
        generator.throw(ex)

def prepare_browsers(headless: bool, driver_path: str) -> Browsers:
    """
    Sets up browsers to search accounts
    :param headless bool: Should search be performed in headless mode
    :return: tuple of browsers, that are logged in LinkedIn and Xing
    """
    driver_path = driver_path if driver_path else "geckodriver"
    profile = FirefoxProfile()
    profile.set_preference("intl.accept_languages", "en-US,en;q=0.5")
    profile.update_preferences()
    logins = social_media_logins(driver_path, profile)
    driver_options = FirefoxOptions()
    driver_options.headless = headless
    linked_in_driver = Firefox(
        options=driver_options,
        firefox_profile=profile,
        executable_path=driver_path)
    xing_driver = Firefox(
        options=driver_options,
        firefox_profile=profile,
        executable_path=driver_path)
    twitter_driver = Firefox(
        options=driver_options,
        firefox_profile=profile,
        executable_path=driver_path)
    set_login_data(linked_in_driver, logins[0])
    set_login_data(xing_driver, logins[1])
    return Browsers(linked_in_driver, xing_driver, twitter_driver)
