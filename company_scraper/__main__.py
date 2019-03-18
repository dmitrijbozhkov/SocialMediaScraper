""" Run app in console """
import argparse
import logging
from company_scraper.manager import init_scrapers, ScraperSettings
from company_scraper.google_news.scraper import GoogleNewsScraper
from company_scraper.kununu.scraper import KununuScraper

parser = argparse.ArgumentParser(description="Application for scraping feedback for a company")
parser.add_argument("-d", "--debugging", help="runs application in debug mode (will log debug logs into console)", action="store_true")
parser.add_argument("-l", "--language", help="Set language for news articles ('en' or 'de')", required=True)
parser.add_argument("-i", "--input", help="Set input file for processing", required=True)
parser.add_argument("-o", "--output", help="Output file for scraping tasks", required=True)
args = parser.parse_args()
if args.debugging:
    logging.basicConfig(level=logging.INFO)
if not (args.language == "en" or args.language == "de"):
    raise RuntimeError("Language should be either 'en' or 'de'")

init_scrapers(args.language, args.output, [
    ScraperSettings(GoogleNewsScraper, args.input),
    ScraperSettings(KununuScraper, args.input)
])
