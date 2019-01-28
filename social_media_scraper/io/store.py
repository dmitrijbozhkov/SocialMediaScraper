""" Database storage pipeline implementation """
from sqlalchemy.orm import scoped_session
from rx import Observable
from social_media_scraper.io.database import store_person_record, store_social_media_record

def store_person(stream: Observable, session_factory: scoped_session):
    """ Stores persons that are red from csv """
    return stream.flat_map(lambda r: Observable.just(store_person_record(session_factory, r)))

def store_social_media(stream: Observable, session_factory: scoped_session):
    """ Stores social media account record """
    return stream.flat_map(lambda r: Observable.just(store_social_media_record(session_factory, r)))
