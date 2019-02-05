# """ Tests for classes, that initialize scraping job """
# from unittest import TestCase
# from unittest.mock import patch, MagicMock, Mock

# class ReadInputTestCase(TestCase):
#     """ Test case for function for reading input file """

#     file_path = "some/path/to/file"

#     @patch("builtins.open")
#     def test_read_input_should_open_file_with_read_mode(self, open_mock):
#         """ Asserts if patch successfull """
#         read_input(self.file_path)
#         open_mock.assert_called_with(self.file_path, "r")

#     @patch("builtins.open")
#     def test_read_input_should_return_file(self, open_mock):
#         """ Asserts that function returns file, thats being open """
#         file_mock = MagicMock()
#         iterable = file_mock.iter.return_value
#         mock_iterator = iter([])
#         iterable.__iter__.return_value = mock_iterator
#         open_mock.side_effect = [file_mock]
#         file, _ = read_input(self.file_path)
#         self.assertEqual(file, file_mock)

#     @patch("csv.reader")
#     @patch("builtins.open")
#     def test_read_input_should_return_stream_of_dicts_from_file(self, open_mock, reader_mock):
#         """ Asserts that function returns file, thats being open """
#         file_record = ["Pepe", "twitter.com", "linkedIn.com", "xing.com"]
#         reader_mock.return_value = [[], file_record]
#         def assert_record(record):
#             self.assertEqual(record["person"], file_record[0])
#             self.assertEqual(record["twitter"], file_record[1])
#             self.assertEqual(record["linkedIn"], file_record[2])
#             self.assertEqual(record["xing"], file_record[3])
#         open_mock.side_effect = [reader_mock]
#         _, stream = read_input(self.file_path)
#         stream.subscribe(assert_record)
#         stream.connect()

#     @patch("csv.reader")
#     @patch("builtins.open")
#     def test_read_input_should_skip_label_row(self, open_mock, reader_mock):
#         """ Asserts that function returns file, thats being open """
#         reader_mock.return_value = [[]]
#         open_mock.side_effect = [reader_mock]
#         _, stream = read_input(self.file_path)
#         stream.subscribe(self.assertFalse)
#         stream.connect()

# class PrepareDatabaseTestCase(TestCase):
#     """ Test case for prepare_database """

#     database_path = ":memory:"
#     db = None

#     def tearDown(self):
#         """ Close database """
#         self.db.engine.dispose()

#     def test_prepare_database_should_create_engine_wth_sqlite_connection_string(self):
#         """ prepare_database should call create engine with correct connection path """
#         self.db = prepare_database(self.database_path)
#         self.assertEqual(str(self.db.engine.url), "sqlite:///" + self.database_path)

#     def test_prepare_database_should_create_scoped_session_factory_with_provided_engine(self):
#         """ prepare_database should return scoped factory binded on created engine """
#         self.db = prepare_database(self.database_path)
#         self.assertEqual(self.db.scoped_factory.get_bind(), self.db.engine)

# class PrepareDriverTestCase(TestCase):
#     """ Test case for prepare_driver """

#     @patch("social_media_scraper.commons.webdriver.Firefox")
#     @patch("social_media_scraper.commons.set_login_data")
#     @patch("social_media_scraper.commons.social_media_logins")
#     def test_prepare_driver_should_return_firefox_driver_with_headless_option(self, login_mock: MagicMock, set_login: MagicMock, firefox_mock: MagicMock):
#         """ prepare_driver should open firefox driver with Options and set headless """
#         is_visible = False
#         driver = Mock()
#         firefox_mock.return_value = driver
#         result = prepare_driver(is_visible)
#         _, kwargs = firefox_mock.call_args
#         self.assertTrue(kwargs["options"].headless)
#         self.assertEqual(driver, result)

#     @patch("social_media_scraper.commons.webdriver.Firefox")
#     @patch("social_media_scraper.commons.set_login_data")
#     @patch("social_media_scraper.commons.social_media_logins")
#     def test_prepare_driver_should_call_login_social_media(self, login_mock: MagicMock, set_login: MagicMock, firefox_mock: MagicMock):
#         """ prepare_driver should try to login into social media """
#         is_visible = False
#         driver = Mock()
#         firefox_mock.return_value = driver
#         prepare_driver(is_visible)
#         login_mock.assert_called_once()
    
#     @patch("social_media_scraper.commons.webdriver.Firefox")
#     @patch("social_media_scraper.commons.set_login_data")
#     @patch("social_media_scraper.commons.social_media_logins")
#     def test_prepare_driver_should_call_set_login_data_with_driver_and_login_data(self, login_mock: MagicMock, set_login: MagicMock, firefox_mock: MagicMock):
#         """ prepare_driver should try to login into social media """
#         is_visible = False
#         driver = Mock()
#         firefox_mock.return_value = driver
#         logins = Mock()
#         login_mock.return_value = logins
#         prepare_driver(is_visible)
#         set_login.assert_called_once_with(driver, logins)

# class StreamTestCase(TestCase):
#     """ Test case for stream composing functionality """

#     @patch("social_media_scraper.commons.ThreadPoolScheduler")
#     def test_prepare_pool_scheduler_should_set_scheduler_with_optimal_amount_of_threads(self, scheduler_mock: MagicMock):
#         """ prepare_pool_scheduler should initiate ThreadPoolScheduler with amount of cpu's """
#         init_scheduler = Mock()
#         scheduler_mock.return_value = init_scheduler
#         cpu_amount = multiprocessing.cpu_count()
#         result = prepare_pool_scheduler()
#         self.assertEqual(init_scheduler, result)
#         scheduler_mock.assert_called_once_with(cpu_amount)
    
#     @patch("social_media_scraper.commons.TkinterScheduler")
#     def test_run_concurrently_should_subscribe_observer_on_tkinter_thread_and_else_on_provided(self, scheduler_mock: MagicMock):
#         """ run_concurrently should observe on TkinterScheduler, subscribe on provided scheduler and subscribe to observer """
#         observing = Mock()
#         subscribing = Mock()
#         disposable = Mock()
#         stream = Mock()
#         observer_mock = Mock()
#         master_view = Mock()
#         pool_scheduler = Mock()
#         init_scheduler = Mock()
#         scheduler_mock.return_value = init_scheduler
#         stream.observe_on.return_value = observing
#         observing.subscribe_on.return_value = subscribing
#         subscribing.subscribe.return_value = disposable
#         result = run_concurrently(stream, observer_mock, master_view, pool_scheduler)
#         scheduler_mock.assert_called_once_with(master_view)
#         stream.observe_on.assert_called_once_with(init_scheduler)
#         observing.subscribe_on.assert_called_once_with(pool_scheduler)
#         subscribing.subscribe.assert_called_once_with(observer_mock)
#         self.assertEqual(disposable, result)
