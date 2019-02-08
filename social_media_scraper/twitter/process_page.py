""" Browser operations for selenium driver and data gathering """
from datetime import datetime as dt
from collections import namedtuple
from selenium import webdriver
from lxml.html import fromstring
from lxml import etree as tr
from social_media_scraper.commons import to_xpath, scroll_bottom, check_if_present, collect_element
from social_media_scraper.model import (Tweet,
                                        TwitterAccount,
                                        TwitterAccountDetails)

PageContent = namedtuple("PageContent", ["page", "link"])

# Twitter profile selectors
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
# Twitter 
STREAM_HAS_MORE_TWEETS = ".has-more-items"
CONTENT = "#page-container"
ENGLISH_QUERY = "?lang=en"

def scroll_untill_end(driver: webdriver.Chrome):
    """ Scrolls down untill all tweets are loaded """
    while check_if_present(driver, STREAM_HAS_MORE_TWEETS):
        scroll_bottom(driver)

def check_if_retweet(tweet: tr.Element) -> bool:
    """ Checks if tweet is original """
    return bool(tweet.xpath(TWEET_IS_RETWEET))

def get_tweet_datetime(tweet: tr.Element):
    """ Get tweet timestamp and parse it into datetime object """
    time_element = tweet.xpath(TWEET_TIMESTAMP)[0]
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

def prepare_english_link(link: str):
    """ Make twitter interface appear in english """
    return link if ENGLISH_QUERY in link else link + ENGLISH_QUERY

def setup_twitter(driver: webdriver.Chrome, data: dict) -> TwitterAccount:
    """ Prepares twitter page to be scraped """
    driver.get(prepare_english_link(data["twitter"]))
    scroll_untill_end(driver)
    html = driver.find_element_by_css_selector(CONTENT).get_attribute("innerHTML")
    data["twitter"] = PageContent(fromstring(html), data["twitter"])
    return data

def collect_tweets(page):
    """ Collects tweet data """
    tweets = []
    for tweet in page.xpath(TWEETS):
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

def collect_twitter(data: dict):
    """ Gathers data from twitter page """
    page = data["twitter"].page
    tweet_amount = collect_element(page, TWEET_AMOUNT)
    subscriptions_amount = collect_element(page, SUBSCRIPTIONS_AMOUNT)
    subscribers_amount = collect_element(page, SUBSCRIBERS_AMOUNT)
    likes_amount = collect_element(page, PROFILE_LIKES_AMOUNT)
    account = TwitterAccount(
        twitterAccountId=data["twitter"].link,
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
    data["twitter"] = account
    return data
