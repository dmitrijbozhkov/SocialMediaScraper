""" Run program """
import argparse
import logging
from social_media_scraper.run import run

parser_description = """
Settings for application
Example usage:
python -m social_media_scraper -m full -i "./example-identification.csv" -o "./output.db" -lb 1 -ub 3 -d -s -g "/path/to/driver/geckodriver.exe"
"""

parser = argparse.ArgumentParser(description=parser_description)

parser.add_argument("-m", "--mode", help="Scrape user account, match identity by data or both (pass acc, id or full respectively)", type=str, required=True)
parser.add_argument("-i", "--input", help="Input file location", type=str)
parser.add_argument("-o", "--output", help="Output file location", type=str)
parser.add_argument("-lb", "--lower_bound", help="Request frequency lower bound", type=int)
parser.add_argument("-ub", "--upper_bound", help="Request frequency upper bound", type=int)
parser.add_argument("-g", "--geckodriver", type=str, help="Set path for geckodriver")
parser.add_argument("-d", "--debugging", help="Runs application in debug mode (will log debug logs into console)", action="store_true")
parser.add_argument("-s", "--sql", help="Log sql into console", action="store_true")
parser.add_argument("-int", "--interface", help="Run app in account scraping mode with interface", action="store_true")

args = parser.parse_args()

if args.debugging:
    logging.basicConfig(level=logging.INFO)

run(args)
