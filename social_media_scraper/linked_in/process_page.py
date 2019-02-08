""" Browser operations and LinkedIn page profile scraping """
from typing import List
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from lxml.html import fromstring
from social_media_scraper.model import LinkedInAccount, LinkedInWorkExperience, LinkedInEducation
from social_media_scraper.commons import (to_xpath,
                                          scroll_bottom,
                                          check_if_present,
                                          collect_element,
                                          click_all)

# LinkedIn user info page selectors
NAME = to_xpath(".pv-top-card-section__name")
CURRENT_POSITION = to_xpath(".pv-top-card-section__headline")
LOCATION = to_xpath(".pv-top-card-section__location")
EXPERIENCE_RECORD = to_xpath("#experience-section .pv-position-entity")
EDUCATION_RECORD = to_xpath("#education-section .pv-education-entity")
EXPERIENCE_POSITION = to_xpath(".pv-entity__summary-info h3 :nth-child(2)")
EXPERIENCE_COMPANY = to_xpath(".pv-entity__summary-info span.pv-entity__secondary-title")
EXPERIENCE_DATERANGE = to_xpath(".pv-entity__summary-info .pv-entity__date-range :nth-child(2)")
EXPERIENCE_DURATION = to_xpath(".pv-entity__summary-info span.pv-entity__bullet-item-v2")
EXPERIENCE_LOCATION = to_xpath(".pv-entity__summary-info .pv-entity__location :nth-child(2)")
EXPERIENCE_DESCRIPTION = to_xpath(".pv-entity__description")
EXPERIENCE_INNER_TIMELINE = to_xpath(".pv-entity__role-details-container")
TIMELINE_COMPANY = to_xpath(".pv-entity__company-summary-info h3 :nth-child(2)")
TIMELINE_POSITION = to_xpath(".pv-entity__summary-info-v2 h3 :nth-child(2)")
TIMELINE_DATERANGE = to_xpath(".pv-entity__summary-info-v2 .pv-entity__date-range :nth-child(2)")
TIMELINE_DURATION = to_xpath(".pv-entity__summary-info-v2 span.pv-entity__bullet-item-v2")
TIMELINE_LOCATION = to_xpath(".pv-entity__summary-info-v2 .pv-entity__location :nth-child(2)")
TIMELINE_DESCRIPTION = to_xpath(".lt-line-clamp__line")
EDUCATION_FACILITY = to_xpath(".pv-entity__degree-info h3")
EDUCATION_SPECIALTY = to_xpath(".pv-entity__degree-info .pv-entity__fos span:nth-child(2)")
EDUCATION_DEGREE = to_xpath(".pv-entity__degree-info .pv-entity__degree-name span:nth-child(2)")
EDUCATION_DATERANGE = to_xpath(".pv-entity__dates span:nth-child(2)")
# Selectors for preparation
MORE_LOCATOR = ".pv-profile-section__see-more-inline"
LESS_LOCATOR = ".pv-profile-section__see-less-inline"
EXPERIENCE_SECTION = ".pv-experience-section__see-more"
EDUCATION_SECTION = "#education-section .pv-profile-section__actions-inline"
COMPANY_TIMELINE_BUTTONS = ".pv-entity__paging"
EXPERIENCE_DESCRIPTION_MORE = "#experience-section .pv-position-entity .lt-line-clamp__more"
CONTENT = ".pv-content"

def open_list(driver: webdriver.Firefox, element_selector: str, more: str, less: str):
    """ Opens all page lists """
    more_selector = element_selector + " " + more
    less_selector = element_selector + " " + less
    wait = WebDriverWait(driver, 900)
    while check_if_present(driver, more_selector):
        click_all(driver, more_selector)
        wait.until(lambda d: d.find_elements_by_css_selector(more_selector) or \
            d.find_elements_by_css_selector(less_selector))

def setup_linked_in(driver: webdriver.Firefox, data: dict):
    """ Sets up LinkedIn page to be scraped """
    driver.get(data["linkedIn"])
    scroll_bottom(driver)
    try:
        open_list(driver, EXPERIENCE_SECTION, MORE_LOCATOR, LESS_LOCATOR)
    except NoSuchElementException:
        pass
    try:
        open_list(driver, EDUCATION_SECTION, MORE_LOCATOR, LESS_LOCATOR)
    except NoSuchElementException:
        pass
    open_list(driver, COMPANY_TIMELINE_BUTTONS, MORE_LOCATOR, LESS_LOCATOR)
    click_all(driver, EXPERIENCE_DESCRIPTION_MORE)
    html = driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")
    data["linkedIn"] = fromstring(html)
    return data

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
    for experience in page.xpath(EXPERIENCE_RECORD):
        inner = experience.xpath(EXPERIENCE_INNER_TIMELINE)
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
    for education in page.xpath(EDUCATION_RECORD):
        education_records.append(LinkedInEducation(
            facilityName=collect_element(education, EDUCATION_FACILITY),
            degreeName=collect_element(education, EDUCATION_DEGREE),
            specialtyName=collect_element(education, EDUCATION_SPECIALTY),
            dateRange=collect_element(education, EDUCATION_DATERANGE)))
    return education_records

def collect_linked_in(data: dict):
    """ Gathers data rom LinkedIn page """
    page = data["linkedIn"]
    name = collect_element(page, NAME)
    current_position = collect_element(page, CURRENT_POSITION)
    location = collect_element(page, LOCATION)
    experiences = collect_experience(page)
    education_records = collect_education(page)
    data["linkedIn"] = LinkedInAccount(
        name=name,
        currentPosition=current_position,
        locaton=location,
        linkedInWorkExperiences=experiences,
        linkedInEducations=education_records)
    return data
