""" Utilities to work with html page """
import re
import logging
from cssselect import GenericTranslator
from selenium import webdriver

TS = GenericTranslator()

def to_xpath(selector: str) -> str:
    """ Returns css selector for lxml """
    return TS.css_to_xpath(selector)

def extract_number(string: str) -> str:
    """ Searches for first number in string """
    return re.search(r"[-+]?\d*\.\d+|\d+", string).group()

def scroll_bottom(driver: webdriver.Firefox):
    """ Scrolls to the end of the page """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_middle(driver: webdriver.Firefox):
    """ Scrols to the middle of the page """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

def check_if_present(driver: webdriver.Firefox, selector: str):
    """ Checks if element is present on page by css selector """
    return bool(driver.find_elements_by_css_selector(selector))

def collect_element(tree, selector: str, default=""):
    """ Selects first element from html tree by selector and returns its text_content(), or default if element not found """
    elements = tree.xpath(selector)
    if not elements:
        logging.info("Collecting isn't possible by selector: %s", selector)
        return default
    return elements[0].text_content()

def lookup_element(page, selector: str):
    """ Log searching page by selector """
    result = page.xpath(selector)
    if not result:
        logging.info("Select returned empty list by selector: %s", selector)
    return result

def click_all(driver: webdriver.Firefox, selector: str):
    """ Executes javascript script, that will click all elements, found by css selector """
    driver.execute_script("document.querySelectorAll('{}').forEach((e) => e.click());".format(selector))
