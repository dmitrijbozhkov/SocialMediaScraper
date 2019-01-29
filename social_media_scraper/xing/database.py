""" Save data from Xing page processing """
from sqlalchemy.orm import scoped_session
from social_media_scraper.logging import XingLog
from social_media_scraper.model import Person

def store_record(session_factory: scoped_session, data: dict):
    """ Refreshes Person record and attaches titter record to it """
    account = data["xing"]
    session = session_factory()
    person = session.query(Person).filter(Person.personId == data["person"].person_id).one()
    account.person = person
    session.add(account)
    session.commit()
    data["xing"] = XingLog(account.name, account.currentPosition)
    session.close()
    return data