""" Logging functionality """
import multiprocessing
from collections import namedtuple
from tkinter import DISABLED, NORMAL, END, Tk
from rx import Observable, Observer
from rx.concurrency.mainloopscheduler import TkinterScheduler
from rx.concurrency import ThreadPoolScheduler
from social_media_scraper.commons import dispose_resources

PersonLog = namedtuple("PersonLog", ["name", "person_id"])

TwitterLog = namedtuple("TwitterLog", ["name", "atName", "amountTweets"])

LinkedInLog = namedtuple("LinkedInLog", ["name", "position"])

XingLog = namedtuple("XingLog", ["name", "position"])

LOG_PERSON_MESSAGE_TEMPLATE = "Person record stored: {} with id {}\n"

LOG_TWITTER_MESSAGE_TEMPLATE = "Twitter account @{} stored by name {} with {} subscribers\n"

LOG_LINKED_IN_MESSAGE_TEMPLATE = "LinkedIn account of {} stored, currently occupying position: {}\n"

LOG_XING_MESSAGE_TEMPLATE = "Xing account of {} stored, currently occupying position: {}\n"

class LogObserver(Observer):
    """ Logs scraper actions on log window """

    def __init__(self, log_window, database, driver, file):
        self.log_window = log_window
        self.driver = driver
        self.database = database
        self.file = file

    def on_next(self, value):
        """ Write log in window """
        write_window(self.log_window, prepare_message(value))

    def on_completed(self):
        """ Write complete message """
        write_window(self.log_window, "Done!")
        dispose_resources(self.file, self.driver, self.database.engine)

    def on_error(self, error):
        """ Write error message """
        write_window(self.log_window, error)

def write_window(log_window, message):
    """ Appends text to window """
    log_window.config(state=NORMAL)
    log_window.insert(END, message + "\n")
    log_window.config(state=DISABLED)

def prepare_message(data: dict) -> str:
    """ Prepares message for displaying on window """
    message = LOG_PERSON_MESSAGE_TEMPLATE.format(data["person"].name, data["person"].person_id)
    if data["twitter"]:
        message = message + LOG_TWITTER_MESSAGE_TEMPLATE.format(data["twitter"].name, data["twitter"].atName, data["twitter"].amountTweets)
    if data["linkedIn"]:
        message = message + LOG_LINKED_IN_MESSAGE_TEMPLATE.format(data["linkedIn"].name, data["linkedIn"].position)
    if data["xing"]:
        message = message + LOG_XING_MESSAGE_TEMPLATE.format(data["xing"].name, data["xing"].position)
    return message

def run_concurrently(stream: Observable, observer: LogObserver, master: Tk, pool_scheduler):
    """ Subscribe and apply scedulers """
    return stream \
        .observe_on(TkinterScheduler(master)) \
        .subscribe_on(pool_scheduler) \
        .subscribe(observer)

def prepare_pool_scheduler():
    """ Prepares pool scheduler to run concurrently """
    optimal_thread_count = multiprocessing.cpu_count()
    return ThreadPoolScheduler(optimal_thread_count)
