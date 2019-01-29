""" Common code accross program to manage external resources """
from collections import namedtuple
import csv
import re
from typing import List
from rx import Observable
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from cssselect import GenericTranslator
from social_media_scraper.model import Base
from social_media_scraper.login import login_social_media, Credentials

DatabaseDrivers = namedtuple("DatabaseDrivers", ["engine", "scoped_factory"])

def read_input(filename: str) -> dict(person=str, twitter=str, linkedIn=str, xing=str):
    """ Reads input csv file and returns observable """
    file = open(filename)
    records = Observable.defer(lambda: Observable.from_(csv.reader(file))) \
        .skip(1) \
        .map(lambda r: {"person": r[0], "twitter": r[1], "linkedIn": r[2], "xing": r[3]})
    return (file, records)

def prepare_database(path: str) -> DatabaseDrivers:
    """ Initializes database to write into """
    engine = create_engine("sqlite:///" + path)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    scoped_factory = scoped_session(session_factory)
    return DatabaseDrivers(engine, scoped_factory)

def prepare_driver(is_visible: bool, credentials: List[Credentials]) -> webdriver.Firefox:
    """ Setups drivers for each social network """
    driver_options = Options()
    driver_options.headless = not is_visible
    driver = webdriver.Firefox(options=driver_options)
    login_social_media(driver, credentials)
    return driver

def dispose_resources(file, driver, database):
    """ Disposes of used resources """
    file.close()
    driver.close()
    database.dispose()

def to_xpath(selector: str) -> str:
    """ Returns css selector for lxml """
    return GenericTranslator().css_to_xpath(selector)

def skip_empty(func, key: str):
    """ Skips execution if record is empty """
    def _inner_skip_empty(record: dict):
        if record.get(key):
            return func(Observable.just(record))
        return Observable.just(record)
    return _inner_skip_empty

def extract_number(string: str) -> str:
    """ Searches for first number in string """
    return re.search("[-+]?\d*\.\d+|\d+", string).group()