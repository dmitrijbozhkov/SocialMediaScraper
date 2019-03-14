""" Scraper management for creating database and managing scraoing jobs """
import asyncio
LINUX_LOOP = True
try:
    import uvloop
except ModuleNotFoundError:
    LINUX_LOOP = False
from typing import List
from collections import namedtuple

ScraperSettings = namedtuple("ScraperSettings", ["scraper", "input_file", "output_file"])

def init_scrapers(language: str, scrapers: List[ScraperSettings]):
    """ Initializes passed scrapers """
    scraper_tasks = []
    if LINUX_LOOP:
        uvloop.install()
    loop = asyncio.get_event_loop()
    for scraper, input_file, output_file in scrapers:
        temp_scraper = scraper.create_scraper()
        temp_scraper.set_language(language)
        temp_scraper.set_input(input_file)
        temp_scraper.set_output(output_file)
        scraper_tasks.append(loop.create_task(temp_scraper.run()))
    loop.run_until_complete(asyncio.wait(scraper_tasks))
