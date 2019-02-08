""" Functions for composing LinkedIn processing pipeline """
from rx import Observable
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.xing.process_page import setup_xing, collect_xing
from social_media_scraper.logging import XingLog
from social_media_scraper.model import Person

def store_record(session_factory: scoped_session, data: dict):
    """ Refreshes Person record and attaches titter record to it """
    account = data["xing"]
    session = session_factory()
    person = session.query(Person).filter(Person.personId == data["person"].person_id).one()
    account.person = person
    session.add(account)
    session.commit()
    log = XingLog(account.name, account.currentPosition)
    session.close()
    return log

def process_xing(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    return stream \
        .flat_map(lambda r: Observable.just(setup_xing(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_xing(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r))) \
        .share()
