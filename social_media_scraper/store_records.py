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

def store_info_record(session_factory: scoped_session, account_data_key: str, data: dict):
    """ Refreshes Person record and attaches titter record to it """
    account = data[account_data_key]
    session = session_factory()
    person = session.query(Person).filter(Person.personId == data["person"].person_id).one()
    account.person = person
    session.add(account)
    session.commit()
    return account
