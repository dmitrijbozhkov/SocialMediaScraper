""" Tests for common functions """
from unittest.mock import Mock, patch, MagicMock, mock_open, call
from social_media_scraper.external_resources import read_csv, write_csv, throttle_emissions
from pytest import fixture
from sqlalchemy.pool import StaticPool

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
    file_rows = ["sad1", "sad2"]
    file_rows_gen = (r for r in file_rows)
    read.return_value = file_rows_gen
    gen = read_csv(FILENAME, True)
    row = next(gen)
    assert row == "sad2"

@patch("csv.writer")
@patch("builtins.open", new_callable=mock_open)
def test_write_csv_should_open_file_with_name(file: MagicMock, write: MagicMock):
    """ write_csv should open file with provided name in write mode and empty newline """
    gen = write_csv(FILENAME)
    next(gen)
    file.assert_called_once_with(FILENAME, "w", newline="")

@patch("csv.writer")
@patch("builtins.open", new_callable=mock_open)
def test_write_csv_should_write_row_of_sent_list_of_columns(file: MagicMock, write: MagicMock):
    """ write_csv should write passed list of columns in row """
    writer = MagicMock()
    write.return_value = writer
    gen = write_csv(FILENAME)
    next(gen)
    columns = [1, 2, 3]
    gen.send(columns)
    writer.writerow.assert_called_once_with(columns)

@patch("csv.writer")
@patch("builtins.open", new_callable=mock_open)
def test_write_csv_should_write_header_if_provided(file: MagicMock, write: MagicMock):
    """ write_csv should write header when initiated if header row provided """
    writer = MagicMock()
    write.return_value = writer
    header = [1, 2, 3]
    gen = write_csv(FILENAME, header)
    next(gen)
    writer.writerow.assert_called_once_with(header)

# @patch("social_media_scraper.external_resources.create_engine")
# @patch("social_media_scraper.external_resources.sessionmaker")
# def test_database_manager_init_database_should_create_engine_with_path(sessionmaker_mock: MagicMock, create_engine_mock: MagicMock):
#     """ DatabaseManager.init_database should create engine with provided path """
#     base = MagicMock()
#     database_file = "/lel/pepe.db"
#     manager = DatabaseManager(database_file)
#     manager.init_database(base)
#     calls = create_engine_mock.call_args_list
#     assert len(calls) == 1
#     assert calls[0][0][0] == "sqlite:////lel/pepe.db"
#     assert not calls[0][1]["echo"]
#     assert calls[0][1]["poolclass"] is StaticPool
#     assert not calls[0][1]["connect_args"]["check_same_thread"]

# @patch("social_media_scraper.external_resources.create_engine")
# @patch("social_media_scraper.external_resources.sessionmaker")
# def test_database_manager_init_database_should_create_databse_tables(sessionmaker_mock: MagicMock, create_engine_mock: MagicMock):
#     """ DatabaseManager.init_database should call create_all on metadata """
#     base = MagicMock()
#     database_file = "/lel/pepe.db"
#     manager = DatabaseManager(database_file)
#     manager.init_database(base)
#     base.metadata.create_all.assert_called_once_with(manager.engine)

# @patch("social_media_scraper.external_resources.create_engine")
# @patch("social_media_scraper.external_resources.sessionmaker")
# def test_database_manager_init_database_should_create_sessionmaker(sessionmaker_mock: MagicMock, create_engine_mock: MagicMock):
#     """ DatabaseManager.init_database should call sessionmaker with engine """
#     base = MagicMock()
#     database_file = "/lel/pepe.db"
#     manager = DatabaseManager(database_file)
#     manager.init_database(base)
#     sessionmaker_mock.assert_called_once_with(bind=manager.engine, autoflush=False)

# def test_database_manager_write_entity_should_add_entity_in_session():
#     """ DatabaseManager.write_entity should call add on session instance with entity """
#     database_file = "/lel/pepe.db"
#     entity = MagicMock()
#     session_factory_mock = MagicMock()
#     session_mock = MagicMock()
#     session_factory_mock.return_value = session_mock
#     manager = DatabaseManager(database_file)
#     manager.session_factory = session_factory_mock
#     manager.write_entity(entity)
#     session_mock.add.assert_called_once_with(entity)

# def test_database_manager_write_entity_should_close_connection_after_adding_entity():
#     """ DatabaseManager.write_entity should call commit and close after add """
#     database_file = "/lel/pepe.db"
#     entity = MagicMock()
#     session_factory_mock = MagicMock()
#     session_mock = MagicMock()
#     session_factory_mock.return_value = session_mock
#     manager = DatabaseManager(database_file)
#     manager.session_factory = session_factory_mock
#     manager.write_entity(entity)
#     calls = session_mock.mock_calls
#     assert calls == [call.add(entity), call.commit(), call.close()]

# def test_database_manager_dispose_database_should_call_dispose_on_engine():
#     """ DatabaseManager.dispose_database should call dispose on engine """
#     database_file = "/lel/pepe.db"
#     engine = MagicMock()
#     manager = DatabaseManager(database_file)
#     manager.engine = engine
#     manager.dispose_database()
#     engine.dispose.assert_called_once()
