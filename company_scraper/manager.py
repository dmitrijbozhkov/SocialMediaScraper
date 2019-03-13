""" Scraper management for creating database and managing scraoing jobs """
import asyncio
import uvloop
from typing import List
from collections import namedtuple
from company_scraper.google_news.constants import USER_AGENT, ACCEPT_LANGUAGE

ScraperSettings = namedtuple("ScraperSettings", ["scraper", "input_file", "output_file"])

def init_scrapers(language: str, scrapers: List[ScraperSettings]):
    """ Initializes passed scrapers """
    scraper_tasks = []
    uvloop.install()
    loop = asyncio.get_event_loop()
    for scraper, input_file, output_file in scrapers:
        temp_scraper = scraper.create_scraper(USER_AGENT, ACCEPT_LANGUAGE)
        temp_scraper.set_language(language)
        temp_scraper.set_input(input_file)
        temp_scraper.set_output(output_file)
        scraper_tasks.append(loop.create_task(temp_scraper.run()))
    loop.run_until_complete(asyncio.wait(scraper_tasks))
