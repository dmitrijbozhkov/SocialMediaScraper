""" Job manager functionality """
import logging
from concurrent.futures import ThreadPoolExecutor, wait
from social_media_scraper.account.model import Person
from social_media_scraper.linked_in.account.process_page import get_linked_in_page, collect_linked_in_page
from social_media_scraper.twitter.account.process_page import get_twitter_page, collect_twitter_page
from social_media_scraper.xing.account.process_page import get_xing_page, collect_xing_page
from social_media_scraper.external_resources import Browsers

def account_scraper(browsers: Browsers, executor: ThreadPoolExecutor):
    """ Scrape data from passed accounts """
    result = None
    account_links = None
    jobs = None
    while True:
        jobs = {}
        account_links = yield result
        if account_links[1]:
            jobs["twitter"] = executor.submit(
                get_twitter_page,
                browsers.Twitter,
                account_links[1])
        if account_links[2]:
            jobs["linkedIn"] = executor.submit(
                get_linked_in_page,
                browsers.LinkedIn,
                account_links[2])
        if account_links[3]:
            jobs["xing"] = executor.submit(
                get_xing_page,
                browsers.Xing,
                account_links[3])
        wait([jobs[k] for k in jobs])
        result = Person(
            name=account_links[0],
            twitterAccount=collect_twitter_page(
                jobs.get("twitter").result(), account_links[1]) if account_links[1] else None,
            linkedInAccount=collect_linked_in_page(
                jobs.get("linkedIn").result(), account_links[2]) if account_links[2] else None,
            xingAccount=collect_xing_page(jobs.get("xing").result()) if account_links[3] else None)
        logging.info("Person accounts scraped: %s", repr(result))
