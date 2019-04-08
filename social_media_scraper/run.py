""" Parse arguments and run application """
from collections import namedtuple
import logging
import os.path as path
from tkinter import Tk
from social_media_scraper.account.interface import Window
from social_media_scraper.account.job_manager import run_job_manager, RunArgs
from social_media_scraper.identification.setup import run_app

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

def run_account_scraping(args: dict):
    """
    Run application in account scraping mode
    :param parser ArgumentParser: Parsed arguments for startup
    """
    if args.debugging:
        logging.basicConfig(level=logging.INFO)
    if not args.headless_interface:
        root = Tk()
        app = Window(root, args)
        root.geometry()
        root.mainloop()
    else:
        check_common_params_present(args)
        run_args = RunArgs(
            args.input,
            args.output,
            args.lower_bound,
            args.upper_bound,
            args.sql,
            args.geckodriver,
            args.headless,
            None,
            None
        )
        run_job_manager(run_args)

def run_identity_matching(args: dict):
    """
    Run application in account searching mode
    :param parser ArgumentParser: Parsed arguments for startup
    """
    check_common_params_present(args)
    run_app(args)
