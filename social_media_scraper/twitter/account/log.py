""" Functionality for logging stored twitter records """
from social_media_scraper.account.model import TwitterAccountSnapshot

LOG_TWITTER_MESSAGE_TEMPLATE = """
Twitter account @{} stored by name {}
"""

def log_twitter(account_record: TwitterAccountSnapshot):
    """ Recieves account record and returns log as string """
    return LOG_TWITTER_MESSAGE_TEMPLATE.format(
        account_record.atName,
        account_record.name)
