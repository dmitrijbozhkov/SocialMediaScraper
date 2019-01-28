""" Scraper implementaion """
from collections import namedtuple
from selenium import webdriver
from rx import Observable
from selenium.webdriver.firefox.options import Options
from social_media_scraper.scraper.browser_operations import process_twitter

SocialMediaDrivers = namedtuple("SocialMediaDrivers", ["twitter", "linkedIn", "xing"])

def setup_driver(is_visible: bool) -> webdriver.Firefox:
    """ Setups drivers for each social network """
    driver_options = Options()
    driver_options.headless = not is_visible
    driver = webdriver.Firefox(options=driver_options)
    return driver

def twitter_scraper(stream: Observable, driver: webdriver.Chrome):
    """ Compose twitter scraper to record stream """
    return stream \
        .filter(lambda p: p.twitter) \
        .flat_map(lambda r: Observable.just(process_twitter(driver, r.person, r.twitter)))
