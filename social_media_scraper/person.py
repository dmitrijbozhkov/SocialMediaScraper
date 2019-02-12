""" Functions to store Person """
from sqlalchemy.orm import scoped_session
from social_media_scraper.logging import PersonLog
from social_media_scraper.model import Person

def store_person_record(session_factory: scoped_session, data):
    """ Stores person record in order to attach accouns to it """
    session = session_factory()
    person = Person(name=data["person"])
    session.add(person)
    session.commit()
    data["person"] = PersonLog(person.name, person.personId)
    session.close()
    return data
