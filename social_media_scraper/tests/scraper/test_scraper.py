""" Tests for scraper functionality """
from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call
from social_media_scraper.scraper.scraper import setup_driver

class ScraperTestCase(TestCase):
    """ Scraper functionality test case """

    @patch("selenium.webdriver.Chrome")
    def test_setup_drivers_should_set_headless_for_drivers(self, chrome_mock):
        setup_driver(True)
        self.assertTrue(chrome_mock.call_args_list[0][0][0].headless)
        self.assertTrue(chrome_mock.call_args_list[1][0][0].headless)
        self.assertTrue(chrome_mock.call_args_list[2][0][0].headless)

if __name__ == "__main__":
    main()