""" Run program """
import argparse
from social_media_scraper.run import run_account_scraping, run_identity_matching

parser_description = """
Settings for application
Example usage:
python -m social_media_scraper -d -s -g "/path/to/driver/geckodriver"
Set application in debug mode and path to geckodriver, also logs sql into console
"""

parser = argparse.ArgumentParser(description=parser_description)

parser.add_argument("-m", "--mode", help="Scrape user account or match identity by data (pass acc or id respectively)", type=str, required=True)
parser.add_argument("-i", "--input", help="Input file location", type=str)
parser.add_argument("-o", "--output", help="Output file location", type=str)
parser.add_argument("-lb", "--lower_bound", help="Request frequency lower bound", type=int)
parser.add_argument("-ub", "--upper_bound", help="Request frequency upper bound", type=int)
parser.add_argument("-he", "--headless", help="Run browser in headless mode", action="store_true")
parser.add_argument("-g", "--geckodriver", type=str, help="set path for geckodriver")

identity_parser = parser.add_argument_group("Identity parser arguments")
social_media_parser = parser.add_argument_group("Social media parser arguments")

social_media_parser.add_argument("-d", "--debugging", help="runs application in debug mode (will log debug logs into console)", action="store_true")
social_media_parser.add_argument("-s", "--sql", help="log sql into console", action="store_true")
social_media_parser.add_argument("-hi", "--headless_interface", help="Run app in headless mode, you should specify input and output files if set to true", action="store_true")

identity_parser.add_argument("-aa", "--account_amount", help="Amount of accounts to match", type=int)

args = parser.parse_args()

if args.mode == "acc":
    run_account_scraping(args)
elif args.mode == "id":
    run_identity_matching(args)
else:
    raise RuntimeError("Mode should be either 'acc' or 'id'")
