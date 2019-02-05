""" Browser operations for Xing acount data scraping """
from enum import Enum
from selenium import webdriver
from lxml.html import fromstring
from social_media_scraper.commons import to_xpath
from social_media_scraper.model import XingAccount

class XingPageSelectors(Enum):
    """ Xing profile selectors """
    NAME = to_xpath("h2[data-qa='malt-profile-display-name'] > span")
    CURRENT_POSITION = to_xpath("div[data-qa='profile-occupations'] p")
    LOCATION = to_xpath("div[data-qa='profile-location'] p")

CONTENT = "html"

def setup_xing(driver: webdriver.Firefox, data: dict):
    """ Set ups LinkedIn page to be scraped """
    driver.get(data["xing"])
    html = driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")
    data["xing"] = fromstring(html)
    return data

def collect_xing(data: dict):
    """ Gathers data rom LinkedIn page """
    page = data["xing"]
    name = page.xpath(XingPageSelectors.NAME.value)[0]
    current_position = page.xpath(XingPageSelectors.CURRENT_POSITION.value)[0]
    location = page.xpath(XingPageSelectors.LOCATION.value)[0]
    data["xing"] = XingAccount(name=name.text_content(),
                               currentPosition=current_position.text_content(),
                               locaton=location.text_content())
    return data
