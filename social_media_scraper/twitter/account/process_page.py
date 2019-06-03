""" Browser operations for selenium driver and data gathering """
import re
import logging
from datetime import datetime as dt
from collections import namedtuple
from selenium import webdriver
from lxml.html import fromstring
from lxml import etree as tr
from social_media_scraper.twitter.page_elements import *
from social_media_scraper.account.page_utils import (
    scroll_bottom,
    check_if_present,
    collect_element,
    lookup_element)
from social_media_scraper.account.model import (Tweet,
                                        TwitterAccount,
                                        TwitterAccountDetails)

PageContent = namedtuple("PageContent", ["page", "link"])

def scroll_untill_end(driver: webdriver.Chrome):
    """ Scrolls down untill all tweets are loaded """
    while check_if_present(driver, STREAM_HAS_MORE_TWEETS):
        scroll_bottom(driver)

def check_if_retweet(tweet: tr.Element) -> bool:
    """ Checks if tweet is original """
    return bool(lookup_element(tweet, TWEET_IS_RETWEET))

def get_tweet_datetime(tweet: tr.Element):
    """ Get tweet timestamp and parse it into datetime object """
    time_element = lookup_element(tweet, TWEET_TIMESTAMP)[0]
    time_value = time_element.get("data-time-ms")
    timestamp = int(time_value) / 1000
    return dt.fromtimestamp(timestamp)

def search_digit(digit_string: str):
    """ Get digit from string """
    result = re.search(r"[\d.,]+", digit_string)
    if result:
        return float(result.group(0))

def parse_stat_numbers(number_string: str):
    """ Parses tweet statistic numbers """
    result_number = number_string
    if not number_string:
        return result_number
    if "," in number_string:
        result_number = number_string.replace(",", ".")
    if "K" in number_string:
        result_number = search_digit(result_number) * 1000
    elif "M" in number_string:
        result_number = search_digit(result_number) * 1000000
    else:
        result_number = result_number.replace(".", "")
    return int(result_number)

def prepare_english_link(link: str):
    """ Make twitter interface appear in english """
    return link if ENGLISH_QUERY in link else link + ENGLISH_QUERY

def collect_tweets(page):
    """ Collects tweet data """
    tweets = []
    for tweet in lookup_element(page, TWEETS):
        datetime_posted = get_tweet_datetime(tweet)
        is_original = check_if_retweet(tweet)
        comments_amount = parse_stat_numbers(collect_element(tweet, TWEET_AMOUNT_COMMENTS))
        retweets_amount = parse_stat_numbers(collect_element(tweet, TWEET_AMOUNT_RETWEETS))
        likes_amount = parse_stat_numbers(collect_element(tweet, TWEET_AMOUNT_LIKES))
        tweet_record = Tweet(
            text=collect_element(tweet, TWEET_TEXT),
            datetime=datetime_posted,
            isOriginal=is_original,
            amountComments=comments_amount,
            amountRetweets=retweets_amount,
            amountLikes=likes_amount)
        tweets.append(tweet_record)
    return tweets

def get_twitter_page(driver: webdriver.Chrome, link: str) -> TwitterAccount:
    """ Prepares twitter page to be scraped """
    driver.get(prepare_english_link(link))
    scroll_untill_end(driver)
    logging.info("Twitter page is ready!")
    return driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")

def collect_twitter_page(html: str, link: str):
    """ Gathers data from twitter page """
    page = fromstring(html)
    tweet_amount = collect_element(page, TWEET_AMOUNT)
    subscriptions_amount = collect_element(page, SUBSCRIPTIONS_AMOUNT)
    subscribers_amount = collect_element(page, SUBSCRIBERS_AMOUNT)
    likes_amount = collect_element(page, PROFILE_LIKES_AMOUNT)
    account = TwitterAccount(
        twitterAccountId=link,
        name=collect_element(page, PROFILE_NAME),
        atName=collect_element(page, ACCOUNT_NAME))
    account_details = TwitterAccountDetails(
        description=collect_element(page, DESCRIPTION),
        location=collect_element(page, LOCATION),
        registerDate=collect_element(page, REGISTER_DATE),
        amountTweets=parse_stat_numbers(tweet_amount),
        amountSubscriptions=parse_stat_numbers(subscriptions_amount),
        amountSubscribers=parse_stat_numbers(subscribers_amount),
        amountLikes=parse_stat_numbers(likes_amount))
    account.twitterAccountDetails = account_details
    tweets = collect_tweets(page)
    account.tweets = tweets
    return account
