""" Functionality for logging stored xing records """
from social_media_scraper.model import XingAccount

LOG_XING_MESSAGE_TEMPLATE = """
Xing account of {} stored, currently occupying position: {}
"""

def log_xing(account_record: XingAccount):
    """ Recieves account record and returns log as string """
    return LOG_XING_MESSAGE_TEMPLATE.format(
        account_record.name,
        account_record.currentPosition)
