""" Parse arguments and run application """
import os.path as path
from tkinter import Tk
from concurrent.futures import ThreadPoolExecutor
from social_media_scraper.account.interface import Window
from social_media_scraper.external_resources import (
    read_csv,
    write_csv,
    throttle_emissions,
    prepare_browsers,
    database_writer)
from social_media_scraper.identification.process_search import identity_matcher
from social_media_scraper.account.process_scraping import account_scraper
from social_media_scraper.account.model import Base

class ArgumentException(Exception):
    """ Exception for dealing with command-line errors """
    pass

def check_common_params_present(args: dict):
    """
    Check headless parameters
    :param parser ArgumentParser: Parsed arguments for startup
    """
    if not args.input:
        raise ArgumentException("Please provide input file path")
    if not path.isfile(args.input):
        raise ArgumentException("Can't find file by path " + args.input)
    if not args.output:
        raise ArgumentException("Please provide output file path")
    if path.isfile(args.output):
        raise ArgumentException("Output file already exists " + args.output)
    if not args.lower_bound:
        raise ArgumentException("Please provide lower bound for random requests")
    if not args.upper_bound:
        raise ArgumentException("Please provide upper bound for random requests")
    if args.lower_bound > args.upper_bound:
        raise ArgumentException("Lower bound should be smaller, than upper")

def run_from_interface(args: dict):
    """
    Run application in account scraping mode
    :param parser ArgumentParser: Parsed arguments for startup
    """
    root = Tk()
    Window(root, args)
    root.geometry()
    root.mainloop()

def run_command_line(args: dict):
    """
    Run application from command line
    :param args dict: Dictionary with command line parameters
    """
    check_common_params_present(args)
    scraping_steps = []
    executor = ThreadPoolExecutor(3)
    reader = read_csv(args.input, True)
    scraping_steps.append(reader)
    browsers = prepare_browsers(False, args.geckodriver, args.twitter_profile)
    if args.mode == "acc":
        scraper = throttle_emissions(account_scraper(browsers, executor), args.lower_bound, args.upper_bound)
        writer = database_writer(args.output, Base, args.sql)
        scraping_steps.append(scraper)
    elif args.mode == "id":
        matcher = throttle_emissions(identity_matcher(browsers, executor), args.lower_bound, args.upper_bound)
        writer = write_csv(args.output, ["Name", "Twitter", "LinkedIn", "Xing"])
        scraping_steps.append(matcher)
    elif args.mode == "full":
        matcher = throttle_emissions(identity_matcher(browsers, executor), args.lower_bound, args.upper_bound)
        scraper = throttle_emissions(account_scraper(browsers, executor), args.lower_bound, args.upper_bound)
        writer = database_writer(args.output, Base, args.sql)
        scraping_steps.append(matcher)
        scraping_steps.append(scraper)
    else:
        raise RuntimeError("Mode should be either 'acc', 'id' or 'full'")
    scraping_steps.append(writer)
    operation_index = 0
    for step in scraping_steps[1:]:
        next(step)
    for record in scraping_steps.pop(0):
        temp_result = record
        while operation_index < len(scraping_steps):
            temp_result = scraping_steps[operation_index].send(temp_result)
            operation_index += 1
        operation_index = 0
    for step in scraping_steps:
        step.close()
    executor.shutdown()
    browsers.Twitter.quit()
    browsers.LinkedIn.quit()
    browsers.Xing.quit()

def run(args: dict):
    """
    Run both scrapers
    :param args  ArgumentParser: Parsed arguments for startupt function
    """
    if args.mode == "acc" and args.interface:
        run_from_interface(args)
    else:
        run_command_line(args)
