""" Tests for person storing functionality """
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from social_media_scraper.person import store_person_record, process_person
from rx import Observable

class PersonTestCase(TestCase):
    """ Test case for functions, associated with storing Person and passing it down """

    person_name = "Danny"

    def setUp(self):
        self.database_session = Mock()
        self.session_factory = Mock()
        self.record = {"person": self.person_name}

    def test_store_person_record_should_commit_new_person(self):
        """ store_person_record should add new person record, commit it and close session """
        self.session_factory.return_value = self.database_session
        store_person_record(self.session_factory, self.record)
        added_record = self.database_session.add.call_args
        self.database_session.commit.assert_called_once()
        self.database_session.close.assert_called_once()
        self.assertEqual(self.person_name, added_record[0][0].name)

    def test_store_person_record_should_return_record_with_PersonLog(self):
        """ store_person_record should store person and return PersonLog named tuple """
        self.session_factory.return_value = self.database_session
        result = store_person_record(self.session_factory, self.record)
        self.assertEqual(self.person_name, result["person"].name) #pylint: disable=no-member

    @patch("social_media_scraper.person.store_person_record")
    def test_process_person_should_compose_store_person_record_to_observable(self, store_mock: MagicMock):
        """ process_person should compose observable to store person records """
        stream = Observable.just(self.record)
        processed = process_person(stream, self.session_factory)
        processed.subscribe()
        store_mock.assert_called_once_with(self.session_factory, self.record)
