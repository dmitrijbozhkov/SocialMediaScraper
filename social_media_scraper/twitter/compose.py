""" Functions for composing twitter processing pipeline """
from rx import Observable
from selenium import webdriver
from sqlalchemy.orm import scoped_session
from social_media_scraper.twitter.process_page import setup_twitter, collect_twitter
from social_media_scraper.logging import TwitterLog
from social_media_scraper.model import Person

def store_record(session_factory: scoped_session, data: dict):
    """ Refreshes Person record and attaches titter record to it """
    account = data["twitter"]
    session = session_factory()
    person = session.query(Person).filter(Person.personId == data["person"].person_id).one()
    account.person = person
    session.add(account)
    session.commit()
    log = TwitterLog(account.name, account.atName, account.twitterAccountDetails.amountTweets)
    session.close()
    return log

def process_twitter(stream: Observable, driver: webdriver.Firefox, session_factory: scoped_session):
    """ Applies twitter processing to only those records, that have twitter link """
    return stream \
        .flat_map(lambda r: Observable.just(setup_twitter(driver, r))) \
        .flat_map(lambda r: Observable.just(collect_twitter(r))) \
        .flat_map(lambda r: Observable.just(store_record(session_factory, r))) \
        .share()
