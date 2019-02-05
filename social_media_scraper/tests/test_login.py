""" Tests login sequence """
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from selenium.webdriver.common.by import By
from social_media_scraper.login import (social_media_logins,
                                        login,
                                        LOGIN_WAIT_TIME,
                                        LINKED_IN_404_PAGE,
                                        XING_404_PAGE,
                                        get_localstorage,
                                        set_localstorage,
                                        LoginData)

class LoginTestCase(TestCase):
    """ Test case for login functionality """

    success_selector = ".success"
    login_link = "login.com"

    def setUp(self):
        self.driver_mock = driver_mock = Mock()

    def test_login_should_go_to_login_page(self):
        """ login function should open login page """
        login(self.driver_mock, self.success_selector, self.login_link)
        self.driver_mock.get.assert_called_once_with(self.login_link)

    @patch("social_media_scraper.login.WebDriverWait")
    def test_login_should_wait_until_success_element_shows_up(self, wait_mock: MagicMock):
        """ login should wait until success element is located on a page """
        waiter = Mock()
        wait_mock.return_value = waiter
        login(self.driver_mock, self.success_selector, self.login_link)
        wait_mock.assert_called_once_with(self.driver_mock, LOGIN_WAIT_TIME)
        until_conditions = waiter.until.call_args_list[0][0][0].locator
        self.assertEqual(By.CSS_SELECTOR, until_conditions[0])
        self.assertEqual(self.success_selector, until_conditions[1])
    
    def test_login_should_get_cookies_from_page(self):
        """ login should get all cookies after logging in and return them """
        cookies_dict = {"key": "val"}
        self.driver_mock.get_cookies.return_value = cookies_dict
        browser_data = login(self.driver_mock, self.success_selector, self.login_link)
        self.assertEqual(cookies_dict, browser_data.cookies)

    @patch("social_media_scraper.login.get_localstorage")
    def test_login_should_get_localstorage_records(self, get_localstorage: MagicMock):
        """ login should get all records from localstorage and return them after login """
        localstorage_dict = {"key": "val"}
        get_localstorage.return_value = localstorage_dict
        browser_data = login(self.driver_mock, self.success_selector, self.login_link)
        self.assertEqual(localstorage_dict, browser_data.localstorage)
    
    def test_get_localstorage_should_execute_script_that_returns_localstorage_contents(self):
        """ get_localstorage should call execute_script on driver, that returns dictionary of records """
        get_localstorage(self.driver_mock)
        called = self.driver_mock.execute_script.call_args[0][0]
        self.assertIsInstance(called, str)

    def test_set_localstorage_should_set_localstorage_records(self):
        """ set_localstorage should call execute_script on driver with each record key and value """
        storage_items = { "key1": "value1", "key2": "value2" }
        store_item_script = "window.localStorage.setItem(arguments[0], arguments[1]);"
        set_localstorage(self.driver_mock, storage_items)
        first_record = self.driver_mock.execute_script.call_args_list[0][0]
        second_record = self.driver_mock.execute_script.call_args_list[1][0]
        self.assertEqual(store_item_script, first_record[0])
        self.assertEqual(storage_items[first_record[1]], first_record[2])
        self.assertEqual(store_item_script, second_record[0])
        self.assertEqual(storage_items[second_record[1]], second_record[2])

    @patch("social_media_scraper.login.webdriver.Firefox")
    @patch("social_media_scraper.login.login")
    def test_social_media_logins_should_open_new_browser_and_close_it_after_login(self, login_mock: MagicMock, firefox_mock: MagicMock):
        """ login_social_media should create new browser instance and close it """
        firefox_mock.return_value = self.driver_mock
        social_media_logins()
        firefox_mock.assert_called_once()
        self.driver_mock.close.assert_called_once()

    @patch("social_media_scraper.login.webdriver.Firefox")
    @patch("social_media_scraper.login.login")
    def test_social_media_logins_should_return_login_data(self, login_mock: MagicMock, firefox_mock: MagicMock):
        """ login_social_media should create new browser instance and close it """
        linked_in_login = LoginData({"key": "val"}, {"key": "val"})
        xing_login = LoginData({"key": "val"}, {"key": "val"})
        login_mock.side_effect = [linked_in_login, xing_login]
        logins = social_media_logins()
        self.assertEqual(linked_in_login, logins[LINKED_IN_404_PAGE])
        self.assertEqual(xing_login, logins[XING_404_PAGE])
