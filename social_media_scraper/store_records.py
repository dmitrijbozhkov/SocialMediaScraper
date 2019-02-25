""" Functions to store Person """
from sqlalchemy.orm import scoped_session
from social_media_scraper.model import Person

def store_person_record(session_factory: scoped_session, data):
    """ Stores person record in order to attach accouns to it """
    session = session_factory()
    person = Person(name=data["person"])
    session.add(person)
    session.commit()
    data["person"] = person.personId
    session.close()
    return data

def store_info_record(session_factory: scoped_session, account_data_key: str, data: dict):
    """ Stores social media account record and returns result of get_snapshot method """
    account = data[account_data_key]
    session = session_factory()
    session.add(account)
    person = session.query(Person).filter(Person.personId == data["person"]).one()
    account.person = person
    snapshot = account.get_snapshot()
    session.commit()
    session.close()
    return snapshot
