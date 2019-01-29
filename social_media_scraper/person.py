""" Functions to store Person """
from rx import Observable
from sqlalchemy.orm import scoped_session
from social_media_scraper.logging import PersonLog
from social_media_scraper.model import Person

def store_person_record(session_factory: scoped_session, data: dict) -> dict:
    """ Stores person record in order to attach accouns to it """
    session = session_factory()
    person = Person(name=data["person"])
    session.add(person)
    session.commit()
    data["person"] = PersonLog(person.name, person.personId)
    session.close()
    return data

def process_person(stream: Observable, session_factory: scoped_session):
    """ Applies saving person record """
    return stream \
        .flat_map(lambda r: Observable.just(store_person_record(session_factory, r)))
