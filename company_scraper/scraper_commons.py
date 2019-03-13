""" Common interfaces for scraper classes """
import csv
from collections import namedtuple
from abc import ABC, abstractmethod

Record = namedtuple("NewsRecord", ["name", "data"])

def read_skip_empty(file_name: str, column: int):
    """ Skips empty rows in column """
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[column]:
                yield Record(row[0], row[column])

def csv_writer(file_name: str):
    """ Writes list of rows into file """
    with open(file_name, "w") as file:
        writer = csv.writer(file, delimiter=",")
        while True:
            row = yield
            if not row:
                break
            writer.writerow(row)

class Scraper(ABC):
    """ Main scraper interface for scraper classes """

    @classmethod
    def create_scraper(cls, user_agent=None, accept_language=None):
        """ Create scraper instance """
        return cls(user_agent=user_agent, accept_language=accept_language)

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
        """ Run event loop in executor """
        raise NotImplementedError("Should implement run")

    @abstractmethod
    def dispose_resources(self):
        """ Called, when after scraping is done """
        raise NotImplementedError("Should implement dispose_resources")