""" Operations, performed in order to get search results from Xing search """
from typing import List
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.xing.page_elements import SEARCH_RESULT_ELEMENT, NO_RESULTS_CONTAINER

SEARCH_LINK = URL("https://www.xing.com/search/members")
NO_MEMBERS_TEXT = "No members found"
GET_SEARCH_RESULTS = r"""
let searchResults = []
let foundElements = document.querySelectorAll("a.Card-style-containerLink-a3b51280")
let tempRecord;
for(let i = 0; i < foundElements.length; i += 1) {
    tempRecord = {
        "link": foundElements[i].href,
        "name": foundElements[i].querySelector("div.MemberCard-style-title-263c10e3").innerText,
        "position": foundElements[i].querySelector("div div:nth-child(2) div div:nth-child(3)").innerText,
        "location": foundElements[i].querySelector("div div:nth-child(2) div div:nth-child(4)").innerText
    };
    searchResults.push(tempRecord);
}
return searchResults;
"""

class XingAccountData(object):
    """ Account data of Xing account """
    def __init__(self):
        self.name = None
        self.position = None
        self.location = None
        self.link = None

    @classmethod
    def create_data(cls, name: str, position: str, location: str, link: str):
        """
        Create account record
        :param name str: Persons name
        :param position str: Persons job
        :param location str: Persons current location
        :param link str: Account link
        :return: Initialized XingAccountData
        """
        account = XingAccountData()
        account.name = name
        account.position = position
        account.location = location
        account.link = link
        return account

def search_xing(driver: Firefox, keywords: str) -> List[XingAccountData]:
    """
    Performs search of people in Xing with provided keywords
    :param driver Firefox: Browser driver to use
    :param keywords str: String of keywords to pass into search field
    :return: List of found profiles
    """
    driver.get(str(SEARCH_LINK.update_query({"keywords": keywords})))
    wait = WebDriverWait(driver, 600)
    wait.until(lambda x: \
        EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT_ELEMENT)) or \
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, NO_RESULTS_CONTAINER), NO_MEMBERS_TEXT))
    results = driver.execute_script(GET_SEARCH_RESULTS)
    accounts = [XingAccountData.create_data(r["name"], r["position"], r["location"], r["link"]) for r in results]
    return accounts
