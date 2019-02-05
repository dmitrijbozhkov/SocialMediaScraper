""" Logging functionality """
from collections import namedtuple
from tkinter import DISABLED, NORMAL, END
from rx import Observer

PersonLog = namedtuple("PersonLog", ["name", "person_id"])

TwitterLog = namedtuple("TwitterLog", ["name", "atName", "amountTweets"])

LinkedInLog = namedtuple("LinkedInLog", ["name", "position"])

XingLog = namedtuple("XingLog", ["name", "position"])

LOG_PERSON_MESSAGE_TEMPLATE = "Person record stored: {} with id {}"
LOG_TWITTER_MESSAGE_TEMPLATE = "Twitter account @{} stored by name {} with {} subscribers"
LOG_LINKED_IN_MESSAGE_TEMPLATE = "LinkedIn account of {} stored, currently occupying position: {}"
LOG_XING_MESSAGE_TEMPLATE = "Xing account of {} stored, currently occupying position: {}"
JOB_COMPLETE_MESSAGE = "Scraping job is done!"

EXCEPTION_TEMPLATE = "Error occured: "

class PersonObserver(Observer):
    """ Logs resource processing on window"""

    def __init__(self, log_window, template):
        self.log_window = log_window
        self.template = template

    def on_next(self, value):
        """ Write log in window """
        write_window(self.log_window, self.template.format(*value))

    def on_completed(self):
        """ Write complete message """
        pass

    def on_error(self, error):
        """ Write error message """
        write_error(self.log_window, error)

class SocialMediaObserver(PersonObserver):
    """ Logs social media processing on window and manages browser """

    def __init__(self, log_window, template, driver):
        super().__init__(log_window, template)
        self.driver = driver

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

    def on_completed(self):
        """ Write complete message """
        write_window(self.log_window, JOB_COMPLETE_MESSAGE)
        self.file.close()
        self.database.dispose()

    def on_error(self, error):
        """ Write error message """
        write_error(self.log_window, error)

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
