""" Tests for common functions """
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from social_media_scraper.commons import (to_xpath,
                                          extract_number,
                                          run_concurrently,
                                          fluctuate,
                                          throttle_filtered,
                                          throttle_random)

class CommonsTestCase(TestCase):
    """ Test case for common functionality """

    def test_dispose_resources_should_dispose_resources(self):
        """ dispose_resources should call close on file and driver and call dispose on database """
        file_mock = Mock()
        driver_mock = Mock()
        database_mock = Mock()
        dispose_resources(file_mock, driver_mock, database_mock)
        file_mock.close.assert_called_once()
        driver_mock.close.assert_called_once()
        database_mock.dispose.assert_called_once()

    def test_to_xpath_should_translate_css_selector_to_xpath(self):
        """ to_xpath should call css_to_xpath on GenericTranslator """
        selector = ".stuff"
        xpath = "descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' stuff ')]"
        result = to_xpath(selector)
        self.assertEqual(xpath, result)
    
    def test_extract_number_should_get_first_number_from_string(self):
        """ extract_number should get first integer or float, separated by dot """
        number_string = "this is lengthy string of 3.14, do you know what does 42 mean?"
        expected = "3.14"
        result = extract_number(number_string)
        self.assertEqual(expected, result)
        
