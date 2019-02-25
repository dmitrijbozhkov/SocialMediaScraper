""" Logging functionality """
from collections import namedtuple
from tkinter import DISABLED, NORMAL, END
from rx import Observer, Observable

JOB_COMPLETE_MESSAGE = "Scraping job is done!"

EXCEPTION_TEMPLATE = "Error occured: " 

class SocialMediaObserver(Observer):
    """ Logs social media processing on window and manages browser """

    def __init__(self, log_window, driver):
        self.log_window = log_window
        self.driver = driver

    def on_next(self, value):
        """ Write log in window """
        write_window(self.log_window, value)

    def on_error(self, error):
        """ Write error message """
        write_error(self.log_window, error)

    def on_completed(self):
        self.driver.close()

class JobObserver(Observer):
    """ Logs job finishing and disposes database and file resources """

    def __init__(self, log_window, database, file):
        self.log_window = log_window
        self.database = database
        self.file = file

    def on_next(self, value):
        """ Write log in window """
        write_window(self.log_window, value)

    def on_error(self, error):
        """ Write error message """
        write_error(self.log_window, error)

    def on_completed(self):
        """ Write complete message """
        write_window(self.log_window, JOB_COMPLETE_MESSAGE)
        self.file.close()
        self.database.scoped_factory.close()
        self.database.engine.dispose()

def log_events(stream: Observable, emit_template: str):
    """ Applies log iterable to template """
    return stream \
        .map(lambda l: emit_template.format(*l))

def write_error(log_window, error):
    """ Writes error message on window """
    return write_window(
        log_window,
        EXCEPTION_TEMPLATE + str(error))

def write_window(log_window, message):
    """ Appends text to window """
    log_window.config(state=NORMAL)
    log_window.insert(END, message + "\n")
    log_window.config(state=DISABLED)
