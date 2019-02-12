""" Functions for composing and storing LinkedIn processing pipeline """
from rx import Observable
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.linked_in.process_page import setup_linked_in, collect_linked_in
from social_media_scraper.logging import LinkedInLog, log_events, LOG_LINKED_IN_MESSAGE_TEMPLATE
from social_media_scraper.model import Person

def store_record(session_factory: scoped_session, data: dict):
    """ Refreshes Person record and attaches titter record to it """
    account = data["linkedIn"]
    session = session_factory()
    person = session.query(Person).filter(Person.personId == data["person"].person_id).one()
    account.person = person
    session.add(account)
    session.commit()
    log = LinkedInLog(account.name, account.currentPosition)
    session.close()
    return log

def process_linked_in(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    processed = stream \
        .flat_map(lambda r: Observable.just(setup_linked_in(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_linked_in(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r))) \
        .share()
    return log_events(processed, LOG_LINKED_IN_MESSAGE_TEMPLATE)
