""" Functionality for logging stored xing records """
from social_media_scraper.model import WorkAccountSnapshot

LOG_XING_MESSAGE_TEMPLATE = """
Xing account of {} stored, currently occupying position: {}
"""

def log_xing(account_record: WorkAccountSnapshot):
    """ Recieves account record and returns log as string """
    return LOG_XING_MESSAGE_TEMPLATE.format(
        account_record.name,
        account_record.currentPosition)
