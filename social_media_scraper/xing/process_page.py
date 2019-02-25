""" Browser operations for Xing acount data scraping """
import json
from datetime import datetime
from functools import reduce
from collections import namedtuple
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from social_media_scraper.commons import scroll_bottom, collect_element
from social_media_scraper.model import XingAccount, XingWorkExperience, XingEducation
from social_media_scraper.xing.page_elements import *

PageContent = namedtuple("PageContent", ["outer", "inner", "link"])

def get_inner_html(driver: webdriver.Firefox):
    """ Get html from inner iframe """
    while not driver.execute_script(INNER_FRAME_READY) == 0:
        driver.implicitly_wait(0.5)
    return driver.execute_script("return document.querySelector('iframe#tab-content').contentWindow.document.body.innerHTML")

def setup_xing(driver: webdriver.Firefox, data: dict):
    """ Set ups LinkedIn page to be scraped """
    driver.get(data["xing"])
    scroll_bottom(driver)
    wait = WebDriverWait(driver, 360)
    wait.until(EC.presence_of_element_located((By.XPATH, NAME)))
    outer_html = driver.find_element_by_css_selector(OUTER_CONTENT).get_attribute("innerHTML")
    inner_html = get_inner_html(driver)
    data["xing"] = PageContent(fromstring(outer_html), fromstring(inner_html), data["xing"])
    return data

def get_content(element):
    """ Get text content from an element without tags """
    return element.text_content()

def compose_list(acc, text):
    """ Composes list of strings """
    return acc + text + ";"

def collect_tags(inner_element):
    """ Collects data from haves and wants lists """
    haves = map(get_content, inner_element.xpath(HAVES))
    wants = map(get_content, inner_element.xpath(WANTS))
    return (
        reduce(compose_list, haves, ""),
        reduce(compose_list, wants, ""))

def get_date_range(experience: dict):
    """ Constructs timestamps from experience """
    begin_year = experience.get("begin_date_year")
    begin_month = experience.get("begin_date_month")
    end_year = experience.get("end_date_year")
    end_month = experience.get("end_date_month")
    begin = None
    end = None
    if begin_year:
        begin = datetime(
            year=begin_year,
            month=begin_month if begin_month else 1,
            day=1)
    if end_year:
        end = datetime(
            year=end_year,
            month=end_month if end_month else 1,
            day=1)
    return (begin, end)

def compose_experience(experience: dict):
    """ Composes XingWorkExperience from input dictionary """
    date_range = get_date_range(experience)
    return XingWorkExperience(
        position=experience.get("job_title"),
        companyName=experience.get("company_name"),
        startDate=date_range[0],
        endDate=date_range[1])

def collect_work_experience(inner_element):
    """ Collects work experience from page """
    work_element = inner_element.xpath(WORK_EXPERIENCE)[0]
    experinece_data = json.loads(work_element.get("value"))
    return list(map(compose_experience, experinece_data))

def compose_education(education: dict):
    """ Compose XingEducation from input dictionary """
    date_range = get_date_range(education)
    return XingEducation(
        degree=education.get("degree"),
        schoolName=education.get("school_name"),
        subject=education.get("subject"),
        schoolNotes=education.get("school_notes"),
        startDate=date_range[0],
        endDate=date_range[1])

def collect_education(inner_element):
    """ Collects education fom page """
    education_element = inner_element.xpath(EDUCATION)[0]
    education_data = json.loads(education_element.get("value"))
    return list(map(compose_education, education_data))

def collect_xing(data: dict):
    """ Gathers data rom LinkedIn page """
    outer_page = data["xing"].outer
    inner_page = data["xing"].inner
    tags = collect_tags(inner_page)
    work_experience = collect_work_experience(inner_page)
    education = collect_education(inner_page)
    data["xing"] = XingAccount(
        xingAccountId=data["xing"].link,
        name=collect_element(outer_page, NAME),
        currentPosition=collect_element(outer_page, CURRENT_POSITION),
        locaton=collect_element(outer_page, LOCATION),
        haves=tags[0],
        wants=tags[1],
        xingWorkExperiences=work_experience,
        xingEducations=education)
    return data
