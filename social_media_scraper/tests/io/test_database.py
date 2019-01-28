""" Tests for database functionality """
import urllib
from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call
from social_media_scraper.io.input import PersonRecord
from social_media_scraper.io.database import prepare_database, store_person_record
from social_media_scraper.io.model import Person

class DatabaseTestCase(TestCase):
    """ Database functionality test case """

    database_path = "/:memory:"

    def setUp(self):
        self.db = prepare_database(self.database_path)
    
    def tearDown(self):
        self.db.engine.dispose()

    def test_prepare_database_should_create_engine_wth_sqlite_connection_string(self):
        """ prepare_database should call create engine with correct connection path """
        db = prepare_database(self.database_path)
        self.assertEqual(str(db.engine.url), "sqlite://" + self.database_path)

    def test_prepare_database_should_create_scoped_session_factory_with_provided_engine(self):
        """ prepare_database should return scoped factory binded on created engine """
        db = prepare_database(self.database_path)
        self.assertEqual(db.scoped_factory.get_bind(), db.engine)

    def test_store_person_record_should_store_user(self):
        """ store_person_record should store user by provided session """
        person_name = "Dennis"
        store_person_record(self.db.scoped_factory, PersonRecord(person_name, "", "", ""))
        session = self.db.scoped_factory()
        record = session.query(Person).filter(Person.name == person_name).one()
        session.close()
        self.assertEqual(record.name, person_name)

    def test_store_person_record_should_return_PersonRecord_with_stored_Person(self):
        """ store_person_record should update PersonRecord with stored Person """
        person_name = "Dennis"
        record = store_person_record(self.db.scoped_factory, PersonRecord(person_name, "", "", ""))
        self.assertIsInstance(record.person, Person)
