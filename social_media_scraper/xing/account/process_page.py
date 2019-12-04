""" Browser operations for Xing acount data scraping """
import json
import logging
from datetime import datetime
from functools import reduce
from collections import namedtuple
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from social_media_scraper.account.page_utils import scroll_bottom, collect_element, lookup_element
from social_media_scraper.account.model import XingAccount, XingWorkExperience, XingEducation
from social_media_scraper.xing.page_elements import *

PageContent = namedtuple("PageContent", ["outer", "inner", "link"])

def get_inner_html(driver: webdriver.Firefox):
    """ Get html from inner iframe """
    while not driver.execute_script(INNER_FRAME_READY) == 0:
        driver.implicitly_wait(0.5)
    return driver.execute_script("return document.querySelector('iframe#tab-content').contentWindow.document.body.innerHTML")

def get_content(element):
    """ Get text content from an element without tags """
    return element.text_content()

def compose_list(acc, text):
    """ Composes list of strings """
    return acc + text + ";"

def collect_tags(inner_element):
    """ Collects data from haves and wants lists """
    haves = map(get_content, lookup_element(inner_element, HAVES))
    wants = map(get_content, lookup_element(inner_element, WANTS))
    return (
        reduce(compose_list, haves, ""),
        reduce(compose_list, wants, ""))

def compose_experience(experience: dict):
    """ Composes XingWorkExperience from input dictionary """
    return XingWorkExperience(
        position=experience["position"],
        companyName=experience["companyName"],
        date=experience["date"])

def collect_work_experience(inner_element):
    """ Collects work experience from page """
    work_entries = lookup_element(inner_element, ENTRY_BOX)[:-1]
    experiences = []
    for entry_box in work_entries:
        for ex in lookup_element(entry_box, ENTRY_SELECTOR):
            experiences.append(compose_experience({
                "position": collect_element(ex, POSITION_SELECTOR),
                "companyName": collect_element(ex, PLACE_SELECTOR),
                "date": collect_element(ex, DATE_SELECTOR)
            }))
    return experiences

def compose_education(education: dict):
    """ Compose XingEducation from input dictionary """
    return XingEducation(
        degree=education["degree"],
        schoolName=education["school_name"],
        subject=education["subject"],
        date=education["date"])

def collect_education(inner_element):
    """ Collects education fom page """
    education_element = lookup_element(inner_element, ENTRY_BOX)[-1]
    educations = []
    for education in lookup_element(education_element, ENTRY_SELECTOR):
        educations.append(compose_education({
            "degree": collect_element(education, POSITION_SELECTOR),
            "school_name": collect_element(education, PLACE_SELECTOR),
            "subject": collect_element(education, EDUCATION_SUBJECT_SELECTOR),
            "date": collect_element(education, DATE_SELECTOR)
        }))
    return educations

def get_xing_page(driver: webdriver.Firefox, link: str):
    """ Set ups LinkedIn page to be scraped """
    driver.get(link)
    scroll_bottom(driver)
    wait = WebDriverWait(driver, 360)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, ENTRY_BOX)))
    inner_html = get_inner_html(driver)
    outer_html = driver.find_element_by_css_selector(OUTER_CONTENT).get_attribute("innerHTML")
    logging.info("Xing page is ready!")
    return PageContent(outer_html, inner_html, link)

def collect_xing_page(data: PageContent):
    """ Gathers data rom LinkedIn page """
    outer_page = fromstring(data.outer)
    inner_page = fromstring(data.inner)
    tags = collect_tags(inner_page)
    work_experience = collect_work_experience(outer_page)
    education = collect_education(outer_page)
    return XingAccount(
        xingAccountId=data.link,
        name=collect_element(outer_page, NAME),
        currentPosition=collect_element(outer_page, CURRENT_POSITION),
        locaton=collect_element(outer_page, LOCATION),
        haves=tags[0],
        wants=tags[1],
        xingWorkExperiences=work_experience,
        xingEducations=education)
