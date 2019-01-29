""" Functions for composing twitter processing pipeline """
from functools import partial
from rx import Observable
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.commons import skip_empty
from social_media_scraper.twitter.process_page import setup_twitter, collect_twitter
from social_media_scraper.twitter.database import store_record

def apply_twitter(driver: webdriver.Firefox, session_factory: scoped_session, stream: Observable):
    """ Applies browser setup processing """
    return stream \
        .flat_map(lambda r: Observable.just(setup_twitter(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_twitter(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r)))

def process_twitter(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    processor = skip_empty(partial(apply_twitter, driver, session_factory), "twitter")
    return stream \
        .flat_map(processor)
