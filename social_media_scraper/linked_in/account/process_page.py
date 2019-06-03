""" Browser operations and LinkedIn page profile scraping """
import logging
from typing import List
from collections import namedtuple
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml.html import fromstring
from social_media_scraper.account.model import LinkedInAccount, LinkedInWorkExperience, LinkedInEducation
from social_media_scraper.linked_in.page_elements import *
from social_media_scraper.account.page_utils import (
    scroll_bottom,
    check_if_present,
    collect_element,
    click_all,
    lookup_element,
    scroll_middle)

PageContent = namedtuple("PageContent", ["page", "link"])

def open_list(driver: webdriver.Firefox, element_selector: str, more: str, less: str):
    """ Opens all page lists """
    more_selector = element_selector + " " + more
    less_selector = element_selector + " " + less
    wait = WebDriverWait(driver, 900)
    while check_if_present(driver, more_selector):
        click_all(driver, more_selector)
        wait.until(lambda d: d.find_elements_by_css_selector(more_selector) or \
            d.find_elements_by_css_selector(less_selector))

def collect_timeline_experience(element, timeline) -> List[LinkedInWorkExperience]:
    """ Parses each wotk experience timeline element and extracts data from it """
    timeline = []
    company = collect_element(element, TIMELINE_COMPANY)
    for experience in timeline:
        work_experience = LinkedInWorkExperience(
            companyName=company,
            position=collect_element(experience, TIMELINE_POSITION),
            dateRange=collect_element(experience, TIMELINE_DATERANGE),
            timeWorked=collect_element(experience, TIMELINE_DURATION),
            location=collect_element(experience, TIMELINE_LOCATION),
            description=collect_element(experience, TIMELINE_DESCRIPTION))
        timeline.append(work_experience)
    return timeline

def collect_experience(page) -> List[LinkedInWorkExperience]:
    """ Parses work experience page elment and extracts data from it """
    experiences = []
    for experience in lookup_element(page, EXPERIENCE_RECORD):
        inner = lookup_element(experience, EXPERIENCE_INNER_TIMELINE)
        if inner:
            experiences.extend(collect_timeline_experience(experience, inner))
        else:
            experiences.append(LinkedInWorkExperience(
                position=collect_element(experience, EXPERIENCE_POSITION),
                companyName=collect_element(experience, EXPERIENCE_COMPANY),
                dateRange=collect_element(experience, EXPERIENCE_DATERANGE),
                timeWorked=collect_element(experience, EXPERIENCE_DURATION),
                location=collect_element(experience, EXPERIENCE_LOCATION),
                description=collect_element(experience, EXPERIENCE_DESCRIPTION)))
    return experiences

def collect_education(page):
    """ Parses persons education page element and extracts data from it """
    education_records = []
    for education in lookup_element(page, EDUCATION_RECORD):
        education_records.append(LinkedInEducation(
            facilityName=collect_element(education, EDUCATION_FACILITY),
            degreeName=collect_element(education, EDUCATION_DEGREE),
            specialtyName=collect_element(education, EDUCATION_SPECIALTY),
            dateRange=collect_element(education, EDUCATION_DATERANGE)))
    return education_records

def get_linked_in_page(driver: webdriver.Firefox, link: str):
    """ Sets up LinkedIn page to be scraped """
    driver.get(link)
    scroll_bottom(driver)
    driver.implicitly_wait(0.5)
    scroll_middle(driver)
    WebDriverWait(driver, 5) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, CONTENT)))
    try:
        WebDriverWait(driver, 5) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, EXPERIENCE_ELEMENT)))
        WebDriverWait(driver, 5) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, EDUCATION_ELEMENT)))
    except TimeoutException:
        pass
    try:
        open_list(driver, EXPERIENCE_SECTION, MORE_LOCATOR, LESS_LOCATOR)
    except NoSuchElementException:
        pass
    try:
        open_list(driver, EDUCATION_SECTION, MORE_LOCATOR, LESS_LOCATOR)
    except NoSuchElementException:
        pass
    open_list(driver, COMPANY_TIMELINE_BUTTONS, MORE_LOCATOR, LESS_LOCATOR)
    click_all(driver, BUTTON_MORE)
    logging.info("LinkedIn page is ready!")
    return driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")

def collect_linked_in_page(html: str, link: str):
    """ Gathers data rom LinkedIn page """
    page = fromstring(html)
    name = collect_element(page, NAME)
    current_position = collect_element(page, CURRENT_POSITION)
    location = collect_element(page, LOCATION)
    experiences = collect_experience(page)
    education_records = collect_education(page)
    return LinkedInAccount(
        linkedInAccountId=link,
        name=name,
        currentPosition=current_position,
        locaton=location,
        linkedInWorkExperiences=experiences,
        linkedInEducations=education_records)
