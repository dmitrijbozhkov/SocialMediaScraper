""" Class for composing scraping job observable """
import csv
import logging
from collections import namedtuple
from rx import Observable
from selenium.webdriver import Firefox
from selenium.common.exceptions import WebDriverException
from sqlalchemy.orm import scoped_session
from social_media_scraper.commons import run_concurrently, throttle_filtered
from social_media_scraper.logging_window import SocialMediaObserver
from social_media_scraper.store_records import store_person_record, store_info_record

JobSchedulers = namedtuple("JobSchedulers", ["tkinter", "pool"])

# Emission messages
READ_EMISSION = "Read emission:"
PERSON_EMISSION = "Person storing emission:"
SETUP_EMISSION = "Setup emission:"
COLLECT_EMISSION = "Collect emission:"
STORE_EMISSION = "Store emission:"
LOG_EMISSION = "Log emission:"
# Error messages
READ_ERROR = "Read error:"
PERSON_ERROR = "Person error:"
SETUP_ERROR = "Setup error:"
COLLECT_ERROR = "Collect error:"
STORE_ERROR = "Store error:"
LOG_ERROR = "Log error:"

def log_next(message: str):
    """ Logs next observable emission """
    return lambda e: logging.info(message + " " + str(e))

def log_error(message: str):
    """ Logs error observable emission """
    return lambda e: logging.error(message + " " + str(e))

class ScrapingJobComposer(object):
    """ Composes scraping observable for website """

    def __init__(self, driver: Firefox, session: scoped_session, schedulers: JobSchedulers):
        self.stream = None
        self.key = None
        self.driver = driver
        self.session = session
        self.schedulers = schedulers

    @staticmethod
    def read_people(session: scoped_session, file):
        """ Initializes csv streaming """
        return Observable.defer(lambda: Observable.from_(csv.reader(file))) \
            .skip(1) \
            .map(lambda r: {"person": r[0], "twitter": r[1], "linkedIn": r[2], "xing": r[3]}) \
            .do_action(log_next(READ_EMISSION), log_error(READ_ERROR)) \
            .map(lambda r: store_person_record(session, r)) \
            .do_action(log_next(PERSON_EMISSION), log_error(PERSON_ERROR)) \
            .publish()

    def set_input(self, input_stream: Observable, data_key: str):
        """ Sets input stream for composing and data key """
        self.stream = input_stream
        self.key = data_key
        return self

    def get_records(self, left_limit: int, right_limit: int):
        """ FIlters appropriate records by key and throttles them between right and left limits """
        self.stream = throttle_filtered(self.stream, self.key, left_limit, right_limit)
        return self

    def process_records(self, setup, collect, log_events):
        """ Compose stream to process records with appropriate functions """
        self.stream = self.stream \
            .map(lambda r: setup(self.driver, r)) \
            .do_action(log_next(SETUP_EMISSION), log_error(SETUP_ERROR)) \
            .map(collect) \
            .do_action(log_next(COLLECT_EMISSION), log_error(COLLECT_ERROR)) \
            .observe_on(self.schedulers.tkinter) \
            .subscribe_on(self.schedulers.pool) \
            .map(lambda r: store_info_record(self.session, self.key, r)) \
            .do_action(log_next(STORE_EMISSION), log_error(STORE_ERROR)) \
            .map(log_events) \
            .do_action(log_next(LOG_EMISSION), log_error(LOG_ERROR)) \
            .share()
        return self

    def subscribe_log(self, log_window):
        """ Subscribes to logging observer and sets scheduler """
        observer = SocialMediaObserver(log_window, self.driver)
        self.stream = self.stream.subscribe(observer)
        return self

    def stop_stream(self):
        """ Disposes subscription and closes browser """
        self.stream.dispose()
        try:
            self.driver.close()
        except WebDriverException:
            logging.debug("Driver already closed")
