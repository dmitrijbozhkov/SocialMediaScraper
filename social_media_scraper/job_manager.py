""" Job manager functionality """
from collections import namedtuple
import csv
from tkinter import Tk
import multiprocessing
from rx import Observable
from rx.concurrency.mainloopscheduler import TkinterScheduler
from rx.concurrency import ThreadPoolScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from social_media_scraper.model import Base
from social_media_scraper.login import social_media_logins, set_login_data
from social_media_scraper.twitter.compose import process_twitter
from social_media_scraper.linked_in.compose import process_linked_in
from social_media_scraper.xing.compose import process_xing
from social_media_scraper.person import store_person_record
from social_media_scraper.commons import run_concurrently, throttle_filtered
from social_media_scraper.logging import (SocialMediaObserver,
                                          JobObserver)

DatabaseDrivers = namedtuple("DatabaseDrivers", ["engine", "scoped_factory"])

BrowserDrivers = namedtuple("BrowserDrivers", ["twitter", "linkedIn", "xing"])

JobSchedulers = namedtuple("JobSchedulers", ["tkinter", "pool"])

class JobManager(object):
    """ Manages running job """

    def __init__(self, file, database, browsers, job, connectable):
        self._file = file
        self._database = database
        self._browsers = browsers
        self._job = job
        self._connectable = connectable

    def begin_scraping(self):
        """ Starts job """
        try:
            self._connectable.connect()
        except AttributeError:
            print("Annoying error, that might occur randomly until rxpy 3 is released, ignore it for now")
            return self
        return self

    def _dispose(self):
        """ Disposes external resources """
        self._file.close()
        self._database.engine.dispose()
        try:
            self._browsers.twitter.close()
            self._browsers.linkedIn.close()
            self._browsers.xing.close()
        except Exception:
            pass

    def stop_scraping(self):
        """ Stops job """
        for job in self._job.keys():
            self._job[job].dispose()
        self._dispose()

class StreamManager(object):
    """ Manages datastreams """

    def __init__(self, database: DatabaseDrivers, browsers: BrowserDrivers):
        self._database: DatabaseDrivers = database
        self._browsers: BrowserDrivers = browsers
        self._datastreams: dict = {}
        self._connectable = None
        self._file = None
        self._schedulers: JobSchedulers = None

    def process_person(self, filename: str):
        """ Prepares input file for reading """
        self._file = open(filename, "r")
        self._connectable = Observable.defer(lambda: Observable.from_(csv.reader(self._file))) \
            .skip(1) \
            .map(lambda r: {"person": r[0], "twitter": r[1], "linkedIn": r[2], "xing": r[3]}) \
            .flat_map(lambda r: Observable.just(store_person_record(self._database.scoped_factory, r))) \
            .publish()
        return self

    def compose_streams(self, left, right):
        """ Composes datastreams """
        person = self._connectable.ref_count()
        twitter_stream = throttle_filtered(person, "twitter", left, right)
        linked_in_stream = throttle_filtered(person, "linkedIn", left, right)
        xing_stream = throttle_filtered(person, "xing", left, right)
        twitter_logs = process_twitter(twitter_stream, self._browsers.twitter, self._database.scoped_factory)
        linked_in_logs = process_linked_in(linked_in_stream, self._browsers.linkedIn, self._database.scoped_factory)
        xing_logs = process_xing(xing_stream, self._browsers.xing, self._database.scoped_factory)
        job_stream = Observable \
            .zip(person, twitter_logs, linked_in_logs, xing_logs, lambda a, b, c, d: a) \
            .ignore_elements()
        self._datastreams = {
            "twitter": twitter_logs,
            "linkedIn": linked_in_logs,
            "xing": xing_logs,
            "job": job_stream
        }
        return self

    def init_schedulers(self, master: Tk):
        """ Initializes schedulers for datastreams """
        optimal_thread_count = multiprocessing.cpu_count()
        pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        tkinter_scheduler = TkinterScheduler(master)
        self._schedulers = JobSchedulers(tkinter_scheduler, pool_scheduler)
        return self

    def init_job(self, log_window) -> JobManager:
        """ Initializes subscribers for prepared datastreams and returns JobManager """
        twitter_sub = SocialMediaObserver(log_window, self._browsers.twitter)
        linked_in_sub = SocialMediaObserver(log_window, self._browsers.linkedIn)
        xing_sub = SocialMediaObserver(log_window, self._browsers.xing)
        job_sub = JobObserver(log_window, self._database.engine, self._file)
        job = {
            "twitter": run_concurrently(self._datastreams["twitter"], twitter_sub, self._schedulers.tkinter, self._schedulers.pool),
            "linkedIn": run_concurrently(self._datastreams["linkedIn"], linked_in_sub, self._schedulers.tkinter, self._schedulers.pool),
            "xing": run_concurrently(self._datastreams["xing"], xing_sub, self._schedulers.tkinter, self._schedulers.pool),
            "job": run_concurrently(self._datastreams["job"], job_sub, self._schedulers.tkinter, self._schedulers.pool)
        }
        return JobManager(self._file, self._database, self._browsers, job, self._connectable)

class BrowserManager(object):
    """ Manages initializing browser """

    def __init__(self, database):
        self._database: DatabaseDrivers = database
        self._browsers: BrowserDrivers = None

    def init_drivers(self, is_visible: bool) -> StreamManager:
        """ Initializes scraper browser drivers """
        logins = social_media_logins()
        driver_options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", "en-us")
        profile.update_preferences()
        driver_options.headless = not is_visible
        self._browsers = BrowserDrivers(
            webdriver.Firefox(options=driver_options, firefox_profile=profile),
            webdriver.Firefox(options=driver_options, firefox_profile=profile),
            webdriver.Firefox(options=driver_options, firefox_profile=profile))
        set_login_data(self._browsers.linkedIn, logins[0])
        set_login_data(self._browsers.xing, logins[1])
        return StreamManager(self._database, self._browsers)

class DatabaseManager(object):
    """ Manages initializing database """

    def __init__(self):
        self._database: DatabaseDrivers = None

    def init_database(self, database_path: str) -> BrowserManager:
        """ Initializes sqlite database to write into """
        engine = create_engine("sqlite:///" + database_path)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        scoped_factory = scoped_session(session_factory)
        self._database = DatabaseDrivers(engine, scoped_factory)
        return BrowserManager(self._database)
