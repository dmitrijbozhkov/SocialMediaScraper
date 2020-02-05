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

def content_check(elements, index, default=None):
    """ Check if elements is in the list and return it """
    return elements[index].text_content() if len(elements) > index else default

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

def collect_work_experience(experience_entries):
    """ Collects work experience from page """
    experiences = []
    for entry_box in experience_entries:
        info_elements = lookup_element(entry_box, INFO_SELECTOR)
        description_selected = lookup_element(entry_box, DESCRIPTION_SELECTOR)
        date = collect_element(entry_box, TIME_SELECTOR)
        experiences.append(XingWorkExperience(
            position=collect_element(entry_box, POSITION_SELECTOR),
            companyName=content_check(info_elements, 2) if date else content_check(info_elements, 1),
            description=content_check(description_selected, 1),
            date=date))
    return experiences

def collect_education(educaion_entries):
    """ Collects education fom page """
    educations = []
    for education in educaion_entries:
        info_elements = lookup_element(education, INFO_SELECTOR)
        date = collect_element(education, TIME_SELECTOR)
        educations.append(XingEducation(
            degree=collect_element(education, POSITION_SELECTOR),
            schoolName=content_check(info_elements, 2) if date else content_check(info_elements, 1),
            subject=content_check(info_elements, 3) if date else content_check(info_elements, 2),
            date=date))
    return educations

def get_xing_page(driver: webdriver.Firefox, link: str):
    """ Set ups LinkedIn page to be scraped """
    driver.get(link)
    scroll_bottom(driver)
    wait = WebDriverWait(driver, 360)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, ENTRIES_LOCATOR)))
    inner_html = get_inner_html(driver)
    outer_html = driver.find_element_by_css_selector(OUTER_CONTENT).get_attribute("innerHTML")
    logging.info("Xing page is ready!")
    return PageContent(outer_html, inner_html, link)

def collect_xing_page(data: PageContent):
    """ Gathers data rom LinkedIn page """
    outer_page = fromstring(data.outer)
    inner_page = fromstring(data.inner)
    tags = collect_tags(inner_page)
    entries = outer_page.xpath(ENTRIES_LOCATOR)
    work_entries = []
    education_entries = []
    is_work = True
    for entry in entries:
        if entry.tag == "h2" and entry.text_content() == "Educational background":
            is_work = False
            continue
        if is_work:
            work_entries.append(entry)
        else:
            education_entries.append(entry)
    work_experience = collect_work_experience(work_entries)
    education = collect_education(education_entries)
    return XingAccount(
        xingAccountId=data.link,
        name=collect_element(outer_page, NAME),
        currentPosition=collect_element(outer_page, CURRENT_POSITION),
        locaton=collect_element(outer_page, LOCATION),
        haves=tags[0],
        wants=tags[1],
        xingWorkExperiences=work_experience,
        xingEducations=education)
