""" Operations, performed in order to get search results from LinkedIn search """
from typing import List
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yarl import URL
from social_media_scraper.linked_in.page_elements import SEARCH_RESULT, NO_RESULT_ELEMENT

SEARCH_LINK = URL("https://www.linkedin.com/search/results/people/")
GET_SEARCH_RESULTS = r"""
let searchResults = []
let foundElements = document.querySelectorAll("li.search-result")
let tempRecord;
let linkElement;
let detailsElements;
let nameElement;
for(let i = 0; i < foundElements.length; i += 1) {
    linkElement = foundElements[i].querySelector("a");
    detailsElements = foundElements[i].querySelectorAll("p");
    nameElement = foundElements[i].querySelector("h3 span.actor-name");
    tempRecord = {
        "link": linkElement.href,
        "name": nameElement.innerText,
        "position": detailsElements[0].innerText,
        "location": detailsElements[1].innerText
    };
    searchResults.push(tempRecord);
}
return searchResults;
"""


class LinkedInAccountData(object):
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
        :return: Initialized LinkedInAccountData
        """
        account = LinkedInAccountData()
        account.name = name
        account.position = position
        account.location = location
        account.link = link
        return account

def search_linked_in(driver: Firefox, keywords: str) -> List[LinkedInAccountData]:
    """
    Performs search of people in LinkedIn with provided keywords
    :param driver Firefox: Browser driver to use
    :param keywords str: String of keywords to pass into search field
    :return: List of found profiles
    """
    driver.get(str(SEARCH_LINK.update_query({"keywords": keywords})))
    wait = WebDriverWait(driver, 600)
    wait.until(lambda x: \
        EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_RESULT)) or \
        EC.presence_of_element_located((By.CSS_SELECTOR, NO_RESULT_ELEMENT)))
    results = driver.execute_script(GET_SEARCH_RESULTS)
    accounts = [LinkedInAccountData.create_data(r["name"], r["position"], r["location"], r["link"]) for r in results]
    return accounts
