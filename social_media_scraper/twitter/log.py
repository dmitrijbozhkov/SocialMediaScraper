""" Functionality for logging stored twitter records """
from social_media_scraper.model import TwitterAccount

LOG_TWITTER_MESSAGE_TEMPLATE = """
Twitter account @{} stored by name {} with {} subscribers
"""

def log_twitter(account_record: TwitterAccount):
    """ Recieves account record and returns log as string """
    return LOG_TWITTER_MESSAGE_TEMPLATE.format(
        account_record.atName,
        account_record.name,
        account_record.twitterAccountDetails.amountSubscribers)
