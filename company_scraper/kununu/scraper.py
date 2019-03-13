""" Kununu scraper functionality """
import os.path as path
import asyncio
from lxml.html import fromstring
from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL
from company_scraper.scraper_commons import Scraper, read_skip_empty, Record, csv_writer
from company_scraper.kununu.constants import SCORE

class KununuScraper(Scraper):
    """ Scraper abstract class implementation for Kununu website """

    def __init__(self, user_agent, accept_language):
        self._user_agent = user_agent
        self._accept_language = accept_language
        self._language = None
        self._input_file = None
        self._output_file = None

    def set_language(self, language: str):
        """ Set scraping language """
        pass

    def set_input(self, input_file: str):
        """ Sets file with links from search queries """
        if not path.isfile(input_file):
            raise RuntimeError("Can't find file by path " + input_file)
        self._input_file = read_skip_empty(input_file, 2)

    def set_output(self, output_file: str):
        """ Set sqlite file path """
        if path.isfile(output_file):
            raise RuntimeError("Output file already exists " + output_file)
        writer = csv_writer(output_file)
        next(writer)
        writer.send(["Company", "Score"])
        self._output_file = writer

    async def _scrape_kununu(self, session, record: Record):
        """ Get kununu page and scrape it """
        try:
            async with session.get(record.data) as response:
                page = await response.text()
                print("Getting resource: " + record.data + " with response: " + str(response.status))
            html = fromstring(page)
            score: str = html.xpath(SCORE)[0].text_content()
            score = float(score.replace(",", "."))
            self._output_file.send([record.name, score])
        except InvalidURL as err:
            print("Fail: " + repr(err))

    async def _init_scraping(self):
        """ Set up scraping kununu """
        loop = asyncio.get_event_loop()
        async with ClientSession() as session:
            tasks = [
                loop.create_task(self._scrape_kununu(session, r))
                for r in self._input_file
            ]
            await asyncio.gather(*tasks)

    async def run(self):
        """ Run scraping process """
        try:
            return await self._init_scraping()
        finally:
            self.dispose_resources()

    def dispose_resources(self):
        """ Dispose output file writer """
        if self._output_file:
            self._output_file.close()