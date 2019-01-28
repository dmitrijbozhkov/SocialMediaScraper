""" Functions for writing into database """
from collections import namedtuple
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from social_media_scraper.io.model import Base, Person, TwitterAccount, LinkedInAccount, XingAccount
from social_media_scraper.io.input import PersonRecord

DatabaseDrivers = namedtuple("DatabaseDrivers", ["engine", "scoped_factory"])

SocialMediaRecord = namedtuple("SocialMediaRecord", ["person_id", "record"])

TwitterRecord = namedtuple("TwitterRecord", ["name", "atName", "amountTweets"])

def prepare_database(path: str) -> DatabaseDrivers:
    """ Initializes database to write into """
    engine = create_engine("sqlite:///" + path)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    scoped_factory = scoped_session(session_factory)
    return DatabaseDrivers(engine, scoped_factory)

def store_social_media_record(session_factory: scoped_session, record: SocialMediaRecord) -> int:
    """ Refreshes Person record and attaches social media to it """
    session = session_factory()
    person = session.query(Person).filter(Person.personId == record.person_id).one()
    record.record.person = person
    session.add(record.record)
    session.commit()
    session.close()
    return record.person_id

def store_person_record(session_factory: scoped_session, person_record: PersonRecord) -> PersonRecord:
    """ Stores person record in order to attach accouns to it """
    session = session_factory()
    session.add(person_record.person)
    session.commit()
    person_id = person_record.person.personId
    session.close()
    return PersonRecord(person_id, person_record.twitter, person_record.linkedIn, person_record.xing)
