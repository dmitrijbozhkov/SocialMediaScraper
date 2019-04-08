""" Job manager functionality """
from collections import namedtuple
from typing import Dict
from tkinter import Tk
import multiprocessing
from rx import Observable
from rx.concurrency.mainloopscheduler import TkinterScheduler
from rx.concurrency import ThreadPoolScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from social_media_scraper.account.model import Base
from social_media_scraper.login import social_media_logins, set_login_data
from social_media_scraper.commons import run_concurrently
from social_media_scraper.account.compose import ScrapingJobComposer, JobSchedulers
from social_media_scraper.linked_in.account.process_page import setup_linked_in, collect_linked_in
from social_media_scraper.twitter.account.process_page import setup_twitter, collect_twitter
from social_media_scraper.xing.account.process_page import setup_xing, collect_xing
from social_media_scraper.linked_in.account.log import log_linked_in
from social_media_scraper.twitter.account.log import log_twitter
from social_media_scraper.xing.account.log import log_xing
from social_media_scraper.account.logging_window import WindowJobObserver, ConsoleJobObserver

DatabaseDrivers = namedtuple("DatabaseDrivers", ["engine", "scoped_factory"])

BrowserDrivers = namedtuple("BrowserDrivers", ["twitter", "linkedIn", "xing"])

RunArgs = namedtuple("RunArgs", [
    "input_file",
    "output_file",
    "request_min",
    "request_max",
    "sql",
    "geckodriver",
    "show_browser",
    "master",
    "debug_field"
])

def run_job_manager(args: RunArgs):
    """"""
    job = DatabaseManager()
    request_min = int(args.request_min)
    request_max = int(args.request_max)
    running_job = job.init_database(args.output_file, args.sql) \
        .init_drivers(args.show_browser, args.geckodriver) \
        .init_schedulers(args.master) \
        .process_person(args.input_file) \
        .compose_streams(request_min, request_max) \
        .init_job(args.debug_field) \
        .begin_scraping()
    return running_job

class JobManager(object):
    """ Manages running job """

    def __init__(self, file, database, streams, jobstream, connectable):
        self._file = file
        self._database = database
        self._streams = streams
        self._jobstream = jobstream
        self._connectable = connectable

    def begin_scraping(self):
        """ Starts job """
        try:
            self._connectable.connect()
            return self
        except AttributeError:
            print("Annoying error, that might occur randomly until rxpy 3 is released, ignore it for now")
            return self

    def _dispose(self):
        """ Disposes external resources """
        self._file.close()
        self._database.scoped_factory.close()
        self._database.engine.dispose()

    def stop_scraping(self):
        """ Stops job """
        for job in self._streams.keys():
            self._streams[job].stop_stream()
        self._jobstream.dispose()
        self._dispose()

class StreamManager(object):
    """ Manages datastreams """

    def __init__(self, database: DatabaseDrivers, browsers: BrowserDrivers):
        self._database: DatabaseDrivers = database
        self._browsers: BrowserDrivers = browsers
        self._datastreams: Dict[str, ScrapingJobComposer] = {}
        self._connectable = None
        self._file = None
        self._schedulers: JobSchedulers = None

    def process_person(self, filename: str):
        """ Prepares input file for reading """
        self._file = open(filename, "r")
        self._connectable = ScrapingJobComposer.read_people(self._database.scoped_factory, self._file)
        return self

    def init_schedulers(self, master: Tk):
        """ Initializes schedulers for datastreams """
        optimal_thread_count = multiprocessing.cpu_count()
        pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        if master:
            tkinter_scheduler = TkinterScheduler(master)
        else:
            tkinter_scheduler = None
        self._schedulers = JobSchedulers(tkinter_scheduler, pool_scheduler)
        return self

    def compose_streams(self, left, right):
        """ Composes datastreams """
        person = self._connectable.ref_count()
        twitter_job = ScrapingJobComposer(
            self._browsers.twitter,
            self._database.scoped_factory,
            self._schedulers) \
            .set_input(person, "twitter") \
            .get_records(left, right) \
            .process_records(setup_twitter, collect_twitter, log_twitter)
        linked_in_job = ScrapingJobComposer(
            self._browsers.linkedIn,
            self._database.scoped_factory,
            self._schedulers) \
            .set_input(person, "linkedIn") \
            .get_records(left, right) \
            .process_records(setup_linked_in, collect_linked_in, log_linked_in)
        xing_job = ScrapingJobComposer(
            self._browsers.xing,
            self._database.scoped_factory,
            self._schedulers) \
            .set_input(person, "xing") \
            .get_records(left, right) \
            .process_records(setup_xing, collect_xing, log_xing)
        job_stream = Observable \
            .zip(twitter_job.stream, linked_in_job.stream, xing_job.stream, lambda a, b, c: a) \
            .ignore_elements()
        self._datastreams = {
            "twitter": twitter_job,
            "linkedIn": linked_in_job,
            "xing": xing_job,
            "job": job_stream
        }
        return self

    def init_job(self, log_window) -> JobManager:
        """ Initializes subscribers for prepared datastreams and returns JobManager """
        if log_window:
            job_sub = WindowJobObserver(log_window, self._database, self._file)
        else:
            job_sub = ConsoleJobObserver(self._database, self._file)
        job = run_concurrently(self._datastreams["job"], job_sub, self._schedulers.tkinter, self._schedulers.pool)
        streams = {
            "twitter": self._datastreams["twitter"].subscribe_log(log_window),
            "linkedIn": self._datastreams["linkedIn"].subscribe_log(log_window),
            "xing": self._datastreams["xing"].subscribe_log(log_window)
        }
        return JobManager(self._file, self._database, streams, job, self._connectable)

class BrowserManager(object):
    """ Manages initializing browser """

    def __init__(self, database):
        self._database: DatabaseDrivers = database
        self._browsers: BrowserDrivers = None

    def init_drivers(self, is_visible: bool, driver_path: str) -> StreamManager:
        """ Initializes scraper browser drivers """
        driver_path = driver_path if driver_path else "geckodriver"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", "en-US,en;q=0.5")
        profile.update_preferences()
        logins = social_media_logins(driver_path, profile)
        driver_options = Options()
        driver_options.headless = not is_visible
        try:
            self._browsers = BrowserDrivers(
            webdriver.Firefox(options=driver_options, firefox_profile=profile, executable_path=driver_path),
            webdriver.Firefox(options=driver_options, firefox_profile=profile, executable_path=driver_path),
            webdriver.Firefox(options=driver_options, firefox_profile=profile, executable_path=driver_path))
        except WebDriverException as ex:
            raise RuntimeError("Seems like wrong geckodriver executable path, error message " + str(ex))
        set_login_data(self._browsers.linkedIn, logins[0])
        set_login_data(self._browsers.xing, logins[1])
        return StreamManager(self._database, self._browsers)

class DatabaseManager(object):
    """ Manages initializing database """

    def __init__(self):
        self._database: DatabaseDrivers = None

    def init_database(self, database_path: str, echo=False) -> BrowserManager:
        """ Initializes sqlite database to write into """
        engine = create_engine(
            "sqlite:///" + database_path,
            echo=echo,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine, autoflush=False)
        self._database = DatabaseDrivers(engine, session_factory)
        return BrowserManager(self._database)
