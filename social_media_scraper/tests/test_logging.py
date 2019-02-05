from unittest import TestCase
from unittest.mock import patch, MagicMock, call, Mock
from tkinter import END, DISABLED, NORMAL
from social_media_scraper.logging import (write_window,
                                          EXCEPTION_TEMPLATE,
                                          write_error,
                                          PersonObserver,
                                          JobObserver,
                                          SocialMediaObserver,
                                          JOB_COMPLETE_MESSAGE)

class LoggingWindowsCase(TestCase):
    """ Test case for window logging functions """

    def test_write_window_should_get_log_window_and_message_and_insert_it(self):
        """ write_window should enable window, append message into it and then disable it """
        window_mock = Mock()
        message = "super message"
        write_window(window_mock, message)
        _, normal_kwargs = window_mock.config.call_args_list[0]
        _, disabled_kwargs = window_mock.config.call_args_list[1]
        self.assertEqual(END, window_mock.insert.call_args[0][0])
        self.assertEqual(message + "\n", window_mock.insert.call_args[0][1])
        self.assertEqual(normal_kwargs["state"], NORMAL)
        self.assertEqual(disabled_kwargs["state"], DISABLED)
    
    @patch("social_media_scraper.logging.write_window")
    def test_write_error_should_call_write_window_with_formatted_error_message(self, write_mock: MagicMock):
        """ write_error should call write_window with log window and format EXCEPTION_TEMPLATE with exception message """
        error = ValueError("message")
        window_mock = Mock()
        write_error(window_mock, error)
        self.assertEqual(window_mock, write_mock.call_args[0][0])
        self.assertEqual(EXCEPTION_TEMPLATE + str(error), write_mock.call_args[0][1])
    
class ProccessObserverTestCase(TestCase):
    """ Test case for ProcessObserver class """

    def setUp(self):
        """ Sets up clean ProcessObserver """
        self.log_window = Mock()
        self.template = Mock()
        self.observer = ProcessObserver(self.log_window, self.template)

    @patch("social_media_scraper.logging.write_window")
    def test_on_next_should_call_write_window_with_log_window_and_format_template(self, write_mock: MagicMock):
        """ on_next should write with formatted template log from processing information """
        message = ("this is log!", "another one!")
        formatted = "message: this is log! another one!"
        self.template.format.return_value = formatted
        self.observer.on_next(message)
        write_mock.assert_called_once_with(self.log_window, formatted)
        self.template.format.assert_called_once_with(message[0], message[1])
    
    @patch("social_media_scraper.logging.write_error")
    def test_on_error_should_call_write_error_with_log_window_and_error(self, write_mock: MagicMock):
        """ on_error should call write_error and pass log_window and error """
        error = ValueError("message")
        self.observer.on_error(error)
        write_mock.assert_called_once_with(self.log_window, error)

class JobObserverTestCase(TestCase):
    """ Test case for JobObserver class """

    def setUp(self):
        """ Sets up clean JobObserver """
        self.log_window = Mock()
        self.database = Mock()
        self.engine = Mock()
        self.database.engine = self.engine
        self.file = Mock()
        self.observer = JobObserver(self.log_window, self.database, self.file)

    @patch("social_media_scraper.logging.write_window")
    def test_on_next_should_call_write_window_with_log_window_and_passed_value(self, write_mock: MagicMock):
        """ on_next should write into log window passed value """
        message = "message"
        self.observer.on_next(message)
        write_mock.assert_called_once_with(self.log_window, message)

    @patch("social_media_scraper.logging.write_error")
    def test_on_error_should_call_write_error_with_log_window_and_error(self, write_mock: MagicMock):
        """ on_error should call write_error and pass log_window and error """
        error = ValueError("message")
        self.observer.on_error(error)
        write_mock.assert_called_once_with(self.log_window, error)

    @patch("social_media_scraper.logging.write_window")
    def test_on_completed_should_call_write_window_with_log_window_and_complete_message(self, write_mock: MagicMock):
        """ on_completed should write JOB_COMPLETE_MESSAGE on debug window """
        self.observer.on_completed()
        write_mock.assert_called_once_with(self.log_window, JOB_COMPLETE_MESSAGE)
    
    @patch("social_media_scraper.logging.dispose_resources")
    @patch("social_media_scraper.logging.write_window")
    def test_on_completed_should_dispose_resouces(self, write_mock: MagicMock, dispose_mock: MagicMock):
        """ on_completed should call dispose_resources with file, driver and engine """
        self.observer.on_completed()
        dispose_mock.assert_called_once_with(self.file, self.driver, self.engine)
