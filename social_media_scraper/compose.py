""" Class for composing scraping job observable """
import csv
from collections import namedtuple
from rx import Observable
from selenium.webdriver import Firefox
from sqlalchemy.orm import scoped_session
from social_media_scraper.commons import run_concurrently, throttle_filtered
from social_media_scraper.logging import SocialMediaObserver
from social_media_scraper.store_records import store_person_record, store_info_record

JobSchedulers = namedtuple("JobSchedulers", ["tkinter", "pool"])

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
        """ Initializes  """
        return Observable.defer(lambda: Observable.from_(csv.reader(file))) \
            .skip(1) \
            .map(lambda r: {"person": r[0], "twitter": r[1], "linkedIn": r[2], "xing": r[3]}) \
            .map(lambda r: store_person_record(session, r)) \
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
            .map(collect) \
            .map(lambda r: store_info_record(self.session, self.key, r)) \
            .map(log_events) \
            .share()
        return self

    def subscribe_log(self, log_window):
        """ Subscribes to logging observer and sets scheduler """
        observer = SocialMediaObserver(log_window, self.driver)
        self.stream = run_concurrently(self.stream, observer, self.schedulers.tkinter, self.schedulers.pool)
        return self

    def stop_stream(self):
        """ Disposes subscription and closes browser """
        self.stream.dispose()
        try:
            self.driver.close()
        except Exception:
            print("Driver already closed!")
