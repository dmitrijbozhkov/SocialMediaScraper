""" Scraper management for creating database and managing scraoing jobs """
import asyncio
from typing import List
from concurrent.futures import ProcessPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from company_scraper.scraper_commons import Scraper
from company_scraper.model import Base

class ScraperSettings(object):
    """ Scraper setting class """
    def __init__(self, scraper: Scraper, input_file: str):
        self.scraper = scraper.create_scraper()
        self.input_file = input_file

    def set_scraper(self, language: str, output_file: str):
        """ Set scraper settings and return task """
        self.scraper.set_language(language)
        self.scraper.set_input(self.input_file)
        self.scraper.set_output(output_file)
        return self.scraper

def init_database(output_file: str):
    """ Initializes database into output file """
    engine = create_engine(
        "sqlite:///" + output_file,
        poolclass=StaticPool)
    Base.metadata.create_all(engine)

async def wait_scrapers(executor, scrapers):
    """ Wait for scrapers in executors """
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, s.run_in_executor)
        for s in scrapers
    ]
    await asyncio.gather(*blocking_tasks)

def init_scrapers(language: str, output_file: str, scrapers: List[ScraperSettings]):
    """ Initializes passed scrapers """
    init_database(output_file)
    Scraper.set_loop()
    loop = asyncio.get_event_loop()
    scraper_instances = []
    for scraper in scrapers:
        scraper_instances.append(scraper.set_scraper(language, output_file))
    executor = ProcessPoolExecutor()
    loop.run_until_complete(wait_scrapers(executor, scraper_instances))
