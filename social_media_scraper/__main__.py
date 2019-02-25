""" Run program """
from tkinter import Tk
import argparse
import logging
from social_media_scraper.interface import Window

parser_description = """
Settings for application
Example usage:
python -m social_media_scraper -d -g "/path/to/driver/geckodriver"
Set application in debug mode and path to geckodriver
"""

parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument("-d", "--debugging", help="runs application in debug mode (will log debug logs into console)", action="store_true")
parser.add_argument("-g", "--geckodriver", type=str, help="set path for geckodriver")
args = parser.parse_args()
if args.debugging:
    logging.basicConfig(level=logging.INFO)

root = Tk()
app = Window(root, args.geckodriver)
root.geometry()
root.mainloop()