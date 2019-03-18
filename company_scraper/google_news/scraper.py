""" Scraper implementation """
import asyncio
import base64
import string
import os.path as path
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import InvalidURL, ClientConnectionError
from yarl import URL
from lxml.html import fromstring
import newspaper
from company_scraper.scraper_commons import Scraper, read_skip_empty, Record, connect_database, ignore_integriy_save
from company_scraper.model import NewsArticle, Company
from company_scraper.google_news.constants import (
    GOOGLE_NEWS_URL,
    GOOGLE_NEWS_DE_SEARCH,
    GOOGLE_NEWS_EN_SEARCH,
    ARTICLE_LINK,
    BROWSER_HEADERS
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

def fix_html_link(link: str):
    """ Fix wrong charcters on links, which end with .html """
    try:
        return link[:link.index(".ht")] + ".html"
    except ValueError:
        return link

def get_first_link(links: str):
    """ Get first link from base64 string """
    index = 0
    length = len(links)
    while index < length:
        if not links[index] in string.printable:
            return links[:index]
        index += 1

def parse_link(link: str):
    """ Parse Google's bullshit """
    decoded = decode_base64(str(link).encode())
    parsed = decoded.decode("utf-8", "ignore")[4:]
    links = str(parsed)
    first_link = get_first_link(links)
    return fix_html_link(first_link)

class GoogleNewsScraper(Scraper):
    """ Scraper implementation for Google News """

    def __init__(self, user_agent, accept_language):
        self._user_agent = user_agent
        self._accept_language = accept_language
        self._language = None
        self._input_file = None
        self._output_file = None
        self._engine = None
        self._sessionmaker = None

    def set_language(self, language: str):
        """ Set language for scraping """
        self._language = language

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

    def _store_article(self, company, link, name, contents, authors, date):
        """ Stores article with SQLAlchemy """
        author_string = ";".join(authors)
        article = NewsArticle(
            newsArticleId=link,
            name=name,
            contents=contents,
            authorString=author_string,
            date=date,
            companyId=company
        )
        ignore_integriy_save(self._sessionmaker(), article)

    def _store_company(self, company):
        """ Store company """
        company = Company(companyId=company)
        ignore_integriy_save(self._sessionmaker(), company)

    async def _read_response(self, response):
        """ Read response by bytes and return string """
        buffer = b""
        async for data in response.content.iter_any():
            buffer += data
        return buffer.decode("utf-8", "ignore")

    async def _scrape_article(self, session, company: str, link: str, name: str):
        """ Scrapes company's articles """
        try:
            link = parse_link(link)
            async with session.get(URL(link, encoded=True)) as response:
                if response.status > 300:
                    raise RuntimeError("Bad response: " + str(response.status))
                page = await self._read_response(response)
                print("Getting resource: " + link + " with response: " + str(response.status))
            article = newspaper.Article(link)
            article.download(input_html=page)
            article.set_meta_language(self._language)
            article.parse()
            self._store_article(company, link, name, article.text, article.authors, article.publish_date)
        except (InvalidURL, asyncio.TimeoutError, RuntimeError, ClientConnectionError) as err:
            print("Url fail: " + repr(err) + " Url is: " + repr(link))

    async def _scrape_google_news(self, session, link: Record):
        """ Scrapes google news page """
        print("Scraping: " + link.name)
        self._store_company(link.name)
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
        self._engine, self._sessionmaker = connect_database(self._output_file)
        self._input_file = read_skip_empty(self._input_file, 1)
        loop = asyncio.get_event_loop()
        queries = [
            Record(r.name, GOOGLE_NEWS_URL + search_query.format(r.data))
            for r in self._input_file
        ]
        timeout = ClientTimeout(total=60 * 2)
        async with ClientSession(headers=BROWSER_HEADERS, timeout=timeout) as session:
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
