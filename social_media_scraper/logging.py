""" Logging functionality """
import multiprocessing
from tkinter import DISABLED, NORMAL, END, Tk
from rx import Observable, Observer
from rx.concurrency.mainloopscheduler import TkinterScheduler
from rx.concurrency import ThreadPoolScheduler
from social_media_scraper.io.model import Person
from social_media_scraper.io.input import PersonRecord
from social_media_scraper.io.database import SocialMediaRecord

class LogObserver(Observer):
    """ Logs scraper actions on log window """

    def __init__(self, log_window, database, drivers, file):
        self.log_window = log_window
        self.drivers = drivers
        self.database = database
        self.file = file

    def on_next(self, value):
        """ Write log in window """
        write_window(self.log_window, "Finished prcessing person with id: " + str(value))

    def on_completed(self):
        """ Write complete message """
        write_window(self.log_window, "Done!")
        dispose_resources(self.file, self.driver, self.database.engine)

    def on_error(self, error):
        """ Write error message """
        self.write_window(error)

def write_window(log_window, message):
    """ Appends text to window """
    log_window.config(state=NORMAL)
    log_window.insert(END, message + "\n")
    log_window.config(state=DISABLED)

def write_person_record(log_window, record: PersonRecord):
    """ Notifies of saving person record """
    person = Person(name=record.person)
    write_window(log_window, "Person will be processed: " + person.name)
    return PersonRecord(person, record.twitter, record.linkedIn, record.xing)

def write_twitter_record(log_window, record: SocialMediaRecord):
    """ Notifies of saving twitter record """
    write_window(
        log_window,
        "Twitter account @{} named {} with {} tweets will be stored".format(
            record.record.atName,
            record.record.name,
            record.record.twitterAccountDetails.amountTweets))
    return record

def log_save_person_record(stream: Observable, log_window, master: Tk, pool_scheduler):
    """ Logs saved people """
    return stream \
        .observe_on(TkinterScheduler(master)) \
        .flat_map(lambda r: Observable.just(write_person_record(log_window, r))) \
        .observe_on(pool_scheduler) \

def log_save_twitter_account(stream: Observable, log_window, master: Tk, pool_scheduler):
    """ Logs saved twitter accounts """
    return stream \
        .observe_on(TkinterScheduler(master)) \
        .flat_map(lambda r: Observable.just(write_twitter_record(log_window, r))) \
        .observe_on(pool_scheduler)

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

def dispose_resources(file, driver, database):
    """ Disposes of used resources """
    file.close()
    driver.close()
    database.dispose()
