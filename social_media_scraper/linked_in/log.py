""" Functionality for logging stored LinkedIn records """
from social_media_scraper.model import LinkedInAccount

LOG_LINKED_IN_MESSAGE_TEMPLATE = """
LinkedIn account of {} stored, currently occupying position: {}
"""

def log_linked_in(account_record: LinkedInAccount):
    """ Recieves account record and returns log as string """
    return LOG_LINKED_IN_MESSAGE_TEMPLATE.format(
        account_record.name,
        account_record.currentPosition)