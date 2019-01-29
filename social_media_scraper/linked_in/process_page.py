""" Browser operations and LinkedIn page profile scraping """
from enum import Enum
from selenium import webdriver
from lxml.html import fromstring
from social_media_scraper.commons import to_xpath
from social_media_scraper.model import LinkedInAccount

class LinkedInPageSelectors(Enum):
    """ LinkedIn profile selectors """
    NAME = to_xpath(".pv-top-card-section__name")
    CURRENT_POSITION = to_xpath(".pv-top-card-section__headline")
    LOCATION = to_xpath(".pv-top-card-section__location")

CONTENT = ".pv-content"

def setup_linked_in(driver: webdriver.Firefox, data: dict):
    """ Set ups LinkedIn page to be scraped """
    driver.get(data["linkedIn"])
    html = driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")
    data["linkedIn"] = fromstring(html)
    return data

def collect_linked_in(data: dict):
    """ Gathers data rom LinkedIn page """
    page = data["linkedIn"]
    name = page.xpath(LinkedInPageSelectors.NAME.value)[0]
    current_position = page.xpath(LinkedInPageSelectors.CURRENT_POSITION.value)[0]
    location = page.xpath(LinkedInPageSelectors.LOCATION.value)[0]
    data["linkedIn"] = LinkedInAccount(name=name.text_content(),
        currentPosition=current_position.text_content(),
        locaton=location.text_content())
    return data
