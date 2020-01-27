""" Methods to login into social media """
from typing import Dict, Tuple
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

LoginData = namedtuple("LoginData", ["cookies", "localstorage", "link"])

LINKED_IN_SUCCESS_ELEMENT = ".feed-container-theme.feed-outlet"
XING_SUCCESS_ELEMENT = "a[class*='Me-Me-profile']"
LINKED_IN_404_PAGE = "https://www.linkedin.com/404"
XING_404_PAGE = "https://xing.com/404"
LINKED_IN_LOGIN_PAGE = "https://www.linkedin.com/uas/login"
XING_LOGIN_PAGE = "https://login.xing.com/"
LOGIN_WAIT_TIME = 3600

def get_localstorage(driver: webdriver.Firefox) -> Dict[str, str]:
    """ Load all data from localstorage """
    return driver.execute_script(r"""var ls = window.localStorage;
    var items = {};
    var key;
    for (var i = 0; i < ls.length; i += 1) {
        key = ls.key(i)
        items[key] = ls.getItem(key);
    }
    return items;""")

def set_localstorage(driver: webdriver.Firefox, storage_items: Dict[str, str]):
    """ Set all localstorage items """
    for key in storage_items.keys():
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);",
                              key,
                              storage_items[key])

def social_media_logins(driver_path: str, profile, options=Options()) -> Tuple[LoginData, LoginData]:
    """ Logs into LinkedIn account with provided credentials """
    try:
        login_driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=driver_path)
    except WebDriverException as ex:
        raise RuntimeError("Seems like wrong geckodriver executable path, error message " + str(ex))
    linked_in = login(login_driver, LINKED_IN_SUCCESS_ELEMENT, LINKED_IN_LOGIN_PAGE, LINKED_IN_404_PAGE)
    xing = login(login_driver, XING_SUCCESS_ELEMENT, XING_LOGIN_PAGE, XING_404_PAGE)
    login_driver.close()
    return (linked_in, xing)

def login(driver: webdriver.Firefox, success_selector, link: str, empty_link: str) -> LoginData:
    """ Logs into provided account """
    driver.get(link)
    wait = WebDriverWait(driver, LOGIN_WAIT_TIME)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, success_selector)))
    cookies = driver.get_cookies()
    localstorage = get_localstorage(driver)
    return LoginData(cookies, localstorage, empty_link)

def set_login_data(driver: webdriver.Firefox, login_data: LoginData):
    """ Goes to 404 page of each site in order to set authentication data """
    driver.get(login_data.link)
    for cookie in login_data.cookies:
        driver.add_cookie(cookie)
    set_localstorage(driver, login_data.localstorage)
