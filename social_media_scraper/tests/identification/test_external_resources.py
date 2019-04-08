""" Tests for common functions """
from unittest.mock import Mock, patch, MagicMock, mock_open
from social_media_scraper.identification.external_resources import read_csv, write_csv, throttle_emissions

FILENAME = "./file.csv"

@patch("csv.reader")
@patch("builtins.open", new_callable=mock_open)
def test_read_csv_should_open_file_in_read_mode(file: MagicMock, read: MagicMock):
    """ read_csv should call open with 'r' mode """
    reader = MagicMock()
    reader.__iter__.return_value = ["sad", "sad"]
    read.return_value = reader
    gen = read_csv(FILENAME)
    next(gen)
    file.assert_called_once_with(FILENAME, "r")

@patch("csv.reader")
@patch("builtins.open", new_callable=mock_open)
def test_read_csv_should_skip_header_if_header_passed_true(file: MagicMock, read: MagicMock):
    """ read_csv should call next on first row if header is true """
    reader = MagicMock()
    reader.__iter__.return_value = ["sad", "sad"]
    read.return_value = reader
    gen = read_csv(FILENAME)
    next(gen)
    file.assert_called_once_with(FILENAME, "r")
