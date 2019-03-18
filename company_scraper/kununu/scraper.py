""" Kununu scraper functionality """
import os.path as path
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from lxml.html import fromstring
from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL, ClientConnectionError
from company_scraper.scraper_commons import Scraper, read_skip_empty, Record, connect_database, ignore_integriy_save
from company_scraper.kununu.constants import SCORE, BROWSER_HEADERS
from company_scraper.model import Company, KununuAccount

class KununuScraper(Scraper):
    """ Scraper abstract class implementation for Kununu website """

    def __init__(self, user_agent, accept_language):
        self._user_agent = user_agent
        self._accept_language = accept_language
        self._language = None
        self._input_file = None
        self._output_file = None
        self._engine = None
        self._sessionmaker = None

    def set_language(self, language: str):
        """ Set scraping language """
        pass

    def set_input(self, input_file: str):
        """ Sets file with links from search queries """
        if not path.isfile(input_file):
            raise RuntimeError("Can't find file by path " + input_file)
        self._input_file = input_file

    def set_output(self, output_file: str):
        """ Set sqlite file path """
        if not path.isfile(output_file):
            raise RuntimeError("Output file doesn't exist " + output_file)
        self._output_file = output_file

    def _store_record(self, company, link, score):
        """ Store KununuAccount instance """
        account = KununuAccount(
            kununuAccountId=link,
            kununuScore=score,
            companyId=company
        )
        ignore_integriy_save(self._sessionmaker(), account)

    # def _store_company(self, company):
    #     """ Store company """
    #     company = Company(companyId=company)
    #     ignore_integriy_save(self._sessionmaker(), company)

    async def _scrape_kununu(self, session, record: Record):
        """ Get kununu page and scrape it """
        # self._store_company(record.name)
        try:
            async with session.get(record.data) as response:
                page = await response.text()
                print("Getting resource: " + record.data + " with response: " + str(response.status))
            html = fromstring(page)
            score: str = html.xpath(SCORE)[0].text_content()
            score = float(score.replace(",", "."))
            self._store_record(record.name, record.data, score)
        except (InvalidURL, asyncio.TimeoutError, RuntimeError, ClientConnectionError) as err:
            print("Url fail: " + repr(err) + " Url is: " + repr(record.data))

    async def _init_scraping(self):
        """ Set up scraping kununu """
        self._engine, self._sessionmaker = connect_database(self._output_file)
        self._input_file = read_skip_empty(self._input_file, 2)
        loop = asyncio.get_event_loop()
        async with ClientSession(headers=BROWSER_HEADERS) as session:
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

    def run_in_executor(self):
        """ Run in executor """
        self.set_loop()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())

    def dispose_resources(self):
        """ Dispose output file writer """
        if self._input_file:
            self._input_file.close()
        if self._engine:
            self._engine.dispose()