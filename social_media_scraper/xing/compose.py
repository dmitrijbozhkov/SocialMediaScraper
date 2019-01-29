""" Functions for composing LinkedIn processing pipeline """
from functools import partial
from rx import Observable
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.commons import skip_empty
from social_media_scraper.xing.process_page import setup_xing, collect_xing
from social_media_scraper.xing.database import store_record

def apply_xing(driver: webdriver.Firefox, session_factory: scoped_session, stream: Observable):
    """ Applies browser setup processing """
    return stream \
        .flat_map(lambda r: Observable.just(setup_xing(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_xing(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r)))

def process_xing(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    processor = skip_empty(partial(apply_xing, driver, session_factory), "xing")
    return stream \
        .flat_map(processor)
