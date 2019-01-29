""" Methods to login into LinkedIn """
from enum import Enum
from typing import List
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#LinkedIn and Xing
#faster.than.fart@gmail.com
#8246ghjK


Credentials = namedtuple("Credentrials", ["username", "password"])

class LinkedInPageSelectors(Enum):
    """ Page selectors for LinkedIn login"""
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON = ".login__form_action_container > button"
    SUCCESS_ELEMENT = ".feed-container-theme.feed-outlet"

class XingPageSelectors(Enum):
    """ Page selectors for Xing login"""
    USERNAME_INPUT = "#login_form_username"
    PASSWORD_INPUT = "#login_form_password"
    SUBMIT_BUTTON = "button[type='submit']"
    SUCCESS_ELEMENT = ".myxing-profile-anchor"

LINKED_IN_LOGIN_PAGE = "https://www.linkedin.com/uas/login"
XING_LOGIN_PAGE = "https://login.xing.com/"

def login_social_media(driver: webdriver.Firefox, credentials: List[Credentials]):
    """ Logs into LinkedIn account with provided credentials """
    login(driver, credentials[0], LinkedInPageSelectors, LINKED_IN_LOGIN_PAGE)
    login(driver, credentials[1], XingPageSelectors, XING_LOGIN_PAGE)

def login(driver: webdriver.Firefox, credentials: Credentials, selectors, link: str):
    """ Logs into provided account """
    driver.get(link)
    username_field = driver.find_element_by_css_selector(selectors.USERNAME_INPUT.value)
    password_field = driver.find_element_by_css_selector(selectors.PASSWORD_INPUT.value)
    submit_button = driver.find_element_by_css_selector(selectors.SUBMIT_BUTTON.value)
    username_field.send_keys(credentials.username)
    password_field.send_keys(credentials.password)
    submit_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors.SUCCESS_ELEMENT.value)))
