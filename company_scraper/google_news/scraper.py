""" Scraper implementation """
import asyncio
import base64
import os.path as path
from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL
from yarl import URL
from lxml.html import fromstring
import newspaper
from company_scraper.scraper_commons import Scraper, read_skip_empty, Record, csv_writer
from company_scraper.google_news.constants import (
    GOOGLE_NEWS_URL,
    GOOGLE_NEWS_DE_SEARCH,
    GOOGLE_NEWS_EN_SEARCH,
    ARTICLE_LINK
)

def _news_link(link: str):
    """ Prepends google news url """
    return link.replace("./articles/", "")

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding:
        data += b"=" * (4 - missing_padding)
    return base64.urlsafe_b64decode(data)

def remove_wrong_characters(link: str):
    """ Remove non-ascii characters from link """
    stripped = link.strip("\x01\x00")
    stripped = stripped.strip("\x01v")
    stripped = stripped.strip("\x01\x7f")
    stripped = stripped.strip("\x01n")
    return stripped

def parse_link(link: str):
    """ Parse Google's bullshit """
    decoded = decode_base64(str(link).encode())
    parsed = decoded.decode("utf-8", "ignore")[4:]
    links = str(parsed)
    try:
        return remove_wrong_characters(links[:len(links.split("http")[1]) + 4])
    except IndexError:
        return remove_wrong_characters(links)

class GoogleNewsScraper(Scraper):
    """ Scraper implementation for Google News """

    def __init__(self, user_agent, accept_language):
        self._user_agent = user_agent
        self._accept_language = accept_language
        self._language = None
        self._input_file = None
        self._output_file = None

    def set_language(self, language: str):
        """ Set language for scraping """
        self._language = language

    def set_input(self, input_file: str):
        """ Sets file with links from search queries """
        if not path.isfile(input_file):
            raise RuntimeError("Can't find file by path " + input_file)
        self._input_file = read_skip_empty(input_file, 1)

    def set_output(self, output_file: str):
        """ Set sqlite file path """
        if path.isfile(output_file):
            raise RuntimeError("Output file already exists " + output_file)
        writer = csv_writer(output_file)
        next(writer)
        writer.send(["Company", "Name", "Contents", "Authors", "Date"])
        self._output_file = writer

    def _store_article(self, company, name, contents, authors, date):
        """ Stores article with SQLAlchemy """
        author_string = ";".join(authors)
        self._output_file.send([company, name, contents, author_string, date])

    async def _scrape_article(self, session, company: str, link: str, name: str):
        """ Scrapes company's articles """
        try:
            link = parse_link(link)
            async with session.get(URL(link, encoded=True)) as response:
                page = await response.text()
                print("Getting resource: " + link + " with response: " + str(response.status))
            article = newspaper.Article(link, language=self._language)
            article.download(input_html=page)
            article.parse()
            self._store_article(company, name, article.text, article.authors, article.publish_date)
        except InvalidURL as err:
            print("Fail: " + repr(err))

    async def _scrape_google_news(self, session, link: Record):
        """ Scrapes google news page """
        print("Scraping: " + link.name)
        async with session.get(link.data) as response:
            page = await response.text()
        html = fromstring(page)
        articles = html.xpath(ARTICLE_LINK)
        loop = asyncio.get_event_loop()
        article_tasks = [
            loop.create_task(self._scrape_article(session, link.name, _news_link(a.get("href")), a.text_content()))
            for a in articles
        ]
        await asyncio.gather(*article_tasks)

    async def _init_scraping(self):
        """ Initializes scraping job """
        if self._language == "en":
            search_query = GOOGLE_NEWS_EN_SEARCH
        elif self._language == "de":
            search_query = GOOGLE_NEWS_DE_SEARCH
        else:
            raise RuntimeError("No language found: " + self._language)
        loop = asyncio.get_event_loop()
        queries = [
            Record(r.name, GOOGLE_NEWS_URL + search_query.format(r.data))
            for r in self._input_file
        ]
        async with ClientSession() as session:
            tasks = [
                loop.create_task(self._scrape_google_news(session, r))
                for r in queries
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
