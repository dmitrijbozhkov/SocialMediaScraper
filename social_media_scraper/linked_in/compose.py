""" Functions for composing LinkedIn processing pipeline """
from rx import Observable
from functools import partial
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.commons import skip_empty
from social_media_scraper.linked_in.process_page import setup_linked_in, collect_linked_in
from social_media_scraper.linked_in.database import store_record

def apply_linked_in(driver: webdriver.Firefox, session_factory: scoped_session, stream: Observable):
    """ Applies browser setup processing """
    return stream \
        .flat_map(lambda r: Observable.just(setup_linked_in(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_linked_in(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r)))

def process_linked_in(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    processor = skip_empty(partial(apply_linked_in, driver, session_factory), "linkedIn")
    return stream \
        .flat_map(processor)
