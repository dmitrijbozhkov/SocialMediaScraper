""" Common interfaces for scraper classes """
import csv
from asyncio import new_event_loop, set_event_loop
from collections import namedtuple
from abc import ABC, abstractmethod
LINUX_LOOP = True
try:
    import uvloop
except ModuleNotFoundError:
    LINUX_LOOP = False
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

Record = namedtuple("NewsRecord", ["name", "data"])

def read_skip_empty(file_name: str, column: int):
    """ Skips empty rows in column """
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[column]:
                yield Record(row[0], row[column])

def connect_database(database_file: str):
    """ Connect to sqlalchemy database """
    engine = create_engine(
        "sqlite:///" + database_file,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False})
    return engine, sessionmaker(bind=engine, autoflush=False)

def ignore_integriy_save(session, record):
    """ Store record and ignore integrity exception """
    try:
        session.add(record)
        session.commit()
        session.close()
    except IntegrityError as err:
        print(err)

class Scraper(ABC):
    """ Main scraper interface for scraper classes """

    @classmethod
    def create_scraper(cls, user_agent=None, accept_language=None):
        """ Create scraper instance """
        return cls(user_agent=user_agent, accept_language=accept_language)

    @staticmethod
    def set_loop():
        """ Set event loop """
        if LINUX_LOOP:
            uvloop.install()
        else:
            loop = new_event_loop()
            set_event_loop(loop)

    def set_language(self, language: str):
        """ Set language for search query """
        raise NotImplementedError("Should implement set_language")

    @abstractmethod
    def set_input(self, input_file: str):
        """ Set input file name for scraping """
        raise NotImplementedError("Should implement set_input")

    @abstractmethod
    def set_output(self, output_file: str):
        """ Set output file name for scraping results """
        raise NotImplementedError("Should implement set_output")

    @abstractmethod
    async def run(self):
        """ Run event loop  """
        raise NotImplementedError("Should implement run")

    @abstractmethod
    def run_in_executor(self):
        """ Run in executor """
        raise NotImplementedError("Should implement run")

    @abstractmethod
    def dispose_resources(self):
        """ Called, when after scraping is done """
        raise NotImplementedError("Should implement dispose_resources")