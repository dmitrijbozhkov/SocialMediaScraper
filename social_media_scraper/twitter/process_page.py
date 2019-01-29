""" Browser operations for selenium driver and data gathering """
from enum import Enum
from datetime import datetime as dt
from selenium import webdriver
from lxml.html import fromstring
from lxml import etree as tr
from selenium.common.exceptions import NoSuchElementException
from social_media_scraper.commons import to_xpath, extract_number
from social_media_scraper.model import (Tweet,
                                        TwitterAccount,
                                        TwitterAccountDetails)

class TwitterPageSelectors(Enum):
    """ Twitter profile selectors """
    PROFILE_NAME = to_xpath(".ProfileHeaderCard-nameLink")
    ACCOUNT_NAME = to_xpath(".ProfileHeaderCard .u-linkComplex-target")
    LOCATION = to_xpath(".ProfileHeaderCard-locationText")
    DESCRIPTION = to_xpath(".ProfileHeaderCard-bio")
    REGISTER_DATE = to_xpath(".ProfileHeaderCard-joinDateText")
    TWEET_AMOUNT = to_xpath("a[data-nav='tweets'] > .ProfileNav-value")
    SUBSCRIPTIONS_AMOUNT = to_xpath("a[data-nav='following'] > .ProfileNav-value")
    SUBSCRIBERS_AMOUNT = to_xpath("a[data-nav='followers'] > .ProfileNav-value")
    PROFILE_LIKES_AMOUNT = to_xpath("a[data-nav='favorites'] > .ProfileNav-value")
    TWEETS = to_xpath(".tweet")
    TWEET_IS_RETWEET = to_xpath(".js-retweet-text")
    TWEET_TIMESTAMP = to_xpath("._timestamp")
    TWEET_TEXT = to_xpath(".js-tweet-text-container")
    TWEET_AMOUNT_COMMENTS = to_xpath(".ProfileTweet-action--reply .ProfileTweet-actionCountForPresentation")
    TWEET_AMOUNT_RETWEETS = to_xpath(".ProfileTweet-action--retweet .ProfileTweet-actionCountForPresentation")
    TWEET_AMOUNT_LIKES = to_xpath(".ProfileTweet-action--favorite .ProfileTweet-actionCountForPresentation")

STREAM_HAS_MORE_TWEETS = ".has-more-items"
CONTENT = "#page-container"

def scroll_untill_end(driver: webdriver.Chrome):
    """ Scrolls down untill all tweets are loaded """
    try:
        while driver.find_element_by_css_selector(STREAM_HAS_MORE_TWEETS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except NoSuchElementException:
        pass

def check_if_retweet(tweet: tr.Element) -> bool:
    """ Checks if tweet is original """
    return bool(tweet.xpath(TwitterPageSelectors.TWEET_IS_RETWEET.value))

def get_tweet_datetime(tweet: tr.Element):
    """ Get tweet timestamp and parse it into datetime object """
    time_element = tweet.xpath(TwitterPageSelectors.TWEET_TIMESTAMP.value)[0]
    time_value = time_element.get("data-time-ms")
    timestamp = int(time_value) / 1000
    return dt.fromtimestamp(timestamp)

def parse_stat_numbers(number: str):
    """ Parses tweet statistic numbers """
    if not number:
        return 0
    if number[-1] == "K":
        return int(float(number[0:-1]) * 1000)
    return int(number)

def setup_twitter(driver: webdriver.Chrome, data: dict) -> TwitterAccount:
    """ Prepares twitter page to be scraped """
    driver.get(data["twitter"])
    scroll_untill_end(driver)
    html = driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")
    data["twitter"] = fromstring(html)
    return data

def collect_twitter(data: dict):
    """ Gathers data from twitter page """
    page = data["twitter"]
    name = page.xpath(TwitterPageSelectors.PROFILE_NAME.value)[0]
    account_name = page.xpath(TwitterPageSelectors.ACCOUNT_NAME.value)[0]
    location = page.xpath(TwitterPageSelectors.LOCATION.value)[0]
    description = page.xpath(TwitterPageSelectors.DESCRIPTION.value)[0]
    register_date = page.xpath(TwitterPageSelectors.REGISTER_DATE.value)[0]
    tweet_amount = page.xpath(TwitterPageSelectors.TWEET_AMOUNT.value)[0]
    subscriptions_amount = page.xpath(TwitterPageSelectors.SUBSCRIPTIONS_AMOUNT.value)[0]
    subscribers_amount = page.xpath(TwitterPageSelectors.SUBSCRIBERS_AMOUNT.value)[0]
    likes_amount = page.xpath(TwitterPageSelectors.PROFILE_LIKES_AMOUNT.value)[0]
    account = TwitterAccount(name=name.text_content(), atName=account_name.text_content())
    account_details = TwitterAccountDetails(
        description=description.text_content(),
        location=location.text_content(),
        registerDate=register_date.text_content(),
        amountTweets=int(extract_number(tweet_amount.text_content())),
        amountSubscriptions=int(extract_number(subscriptions_amount.text_content())),
        amountSubscribers=int(extract_number(subscribers_amount.text_content())),
        amountLikes=likes_amount.text_content())
    account.twitterAccountDetails = account_details
    tweets = []
    for tweet in page.xpath(TwitterPageSelectors.TWEETS.value):
        text = tweet.xpath(TwitterPageSelectors.TWEET_TEXT.value)[0]
        datetime_posted = get_tweet_datetime(tweet)
        is_original = check_if_retweet(tweet)
        comments_element = tweet.xpath(TwitterPageSelectors.TWEET_AMOUNT_COMMENTS.value)[0]
        retweets_element = tweet.xpath(TwitterPageSelectors.TWEET_AMOUNT_RETWEETS.value)[0]
        likes_element = tweet.xpath(TwitterPageSelectors.TWEET_AMOUNT_LIKES.value)[0]
        tweet_record = Tweet(
            text=text.text_content(),
            datetime=datetime_posted,
            isOriginal=is_original,
            amountComments=parse_stat_numbers(comments_element.text_content()),
            amountRetweets=parse_stat_numbers(retweets_element.text_content()),
            amountLikes=parse_stat_numbers(likes_element.text_content()))
        tweets.append(tweet_record)
    account.tweets = tweets
    data["twitter"] = account
    return data
