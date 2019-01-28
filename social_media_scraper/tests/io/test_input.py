""" Test input reading functions """
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from social_media_scraper.io.input import read_input

class InputReaderTestCase(TestCase):
    """ Test case for testing input csv file """

    file_path = "some/path/to/file"

    @patch("builtins.open")
    def test_read_input_should_open_file_with_read_mode(self, open_mock):
        """ Asserts if patch successfull """
        read_input(self.file_path)
        open_mock.assert_called_with(self.file_path, "r")

    @patch("builtins.open")
    def test_read_input_should_return_file(self, open_mock):
        """ Asserts that function returns file, thats being open """
        file_mock = MagicMock()
        iterable = file_mock.iter.return_value
        mock_iterator = iter([])
        iterable.__iter__.return_value = mock_iterator
        open_mock.side_effect = [file_mock]
        file, _ = read_input(self.file_path)
        self.assertEqual(file, file_mock)

    @patch("csv.reader")
    @patch("builtins.open")
    def test_read_input_should_return_stream_of_PersonRecord_from_file(self, open_mock, reader_mock):
        """ Asserts that function returns file, thats being open """
        file_record = ["Pepe", "twitter.com", "linkedIn.com", "xing.com"]
        reader_mock.return_value = [[], file_record]
        open_mock.side_effect = [reader_mock]
        _, stream = read_input(self.file_path)
        record = next(iter(stream.to_blocking()))
        self.assertEqual(record.person, file_record[0])
        self.assertEqual(record.twitter, file_record[1])
        self.assertEqual(record.linkedIn, file_record[2])
        self.assertEqual(record.xing, file_record[3])
    
    @patch("csv.reader")
    @patch("builtins.open")
    def test_read_input_should_skip_label_row(self, open_mock, reader_mock):
        """ Asserts that function returns file, thats being open """
        reader_mock.return_value = [[]]
        open_mock.side_effect = [reader_mock]
        _, stream = read_input(self.file_path)
        with self.assertRaises(StopIteration):
            next(iter(stream.to_blocking()))

if __name__ == "__main__":
    main()
