""" Browser imperative code implementation """
from enum import Enum
from datetime import datetime as dt
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from social_media_scraper.io.database import SocialMediaRecord
from social_media_scraper.io.input import PersonRecord
from social_media_scraper.io.model import (Person,
                                           LinkedInAccount,
                                           XingAccount,
                                           Tweet,
                                           TwitterAccount,
                                           TwitterAccountDetails)

class TwitterPageSelectors(Enum):
    """ Twitter profile selectors """
    PROFILE_NAME = ".ProfileHeaderCard-nameLink"
    ACCOUNT_NAME = ".ProfileHeaderCard .u-linkComplex-target"
    LOCATION = ".ProfileHeaderCard-locationText"
    DESCRIPTION = ".ProfileHeaderCard-bio"
    REGISTER_DATE = ".ProfileHeaderCard-joinDateText"
    TWEET_AMOUNT = "a[data-nav='tweets'] > .ProfileNav-value"
    SUBSCRIPTIONS_AMOUNT = "a[data-nav='following'] > .ProfileNav-value"
    SUBSCRIBERS_AMOUNT = "a[data-nav='followers'] > .ProfileNav-value"
    PROFILE_LIKES_AMOUNT = "a[data-nav='favorites'] > .ProfileNav-value"
    TWEETS = ".tweet"
    TWEET_IS_RETWEET = ".js-retweet-text"
    TWEET_TIMESTAMP = "._timestamp"
    TWEET_TEXT = ".js-tweet-text-container"
    TWEET_AMOUNT_COMMENTS = ".ProfileTweet-action--reply .ProfileTweet-actionCountForPresentation"
    TWEET_AMOUNT_RETWEETS = ".ProfileTweet-action--retweet .ProfileTweet-actionCountForPresentation"
    TWEET_AMOUNT_LIKES = ".ProfileTweet-action--favorite .ProfileTweet-actionCountForPresentation"
    STREAM_HAS_MORE_TWEETS = ".has-more-items"

class LinkedINPageSelectors(Enum):
    """ LinkedIn profile selectors """
    REGISTER_FORM = ".join-form"
    LOGIN_FORM = ".login-form"
    FORM_TOGGLE = "a.form-toggle"
    EMAIL_INPUT_LOGIN = ".login-email"
    PASSWORD_INPUT_LOGIN = ".login-password"
    SUBMIT_LOGIN = "#login-submit"
    NAME = ".pv-top-card-section__name"
    CURRENT_POSITION = ".pv-top-card-section__headline"
    LOCATION = ".pv-top-card-section__location"
    EXPERIENCE_SECTION = "#experience-section"
    EXPERIENCES_SECTION = ".pv-experience-section__see-more"
    LOAD_MORE_EXPERIENCE_BUTTON = ".pv-profile-section__see-more-inline"
    EXPERIENCE_ENTRY = ".pv-position-entity"

class XingPageSelectors(Enum):
    """ Xing profile selectors """
    REGISTER_FORM = ".registration"
    LOGIN_SWITCH = "li[data-tab='login']"
    EMAIL_INPUT_LOGIN = "div#login-form input[name='login_form[username]']"
    PASSWORD_INPUT_LOGIN = "div#login-form input[name='login_form[password]']"
    SUBMIT_LOGIN = "div#login-form div.clfx.mt10 button[type='submit']"

def scroll_untill_end(driver: webdriver.Chrome):
    """ Scrolls down untill all tweets are loaded """
    try:
        while driver.find_element_by_css_selector(TwitterPageSelectors.STREAM_HAS_MORE_TWEETS.value):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except NoSuchElementException:
        pass

def check_if_retweet(tweet: WebElement) -> bool:
    """ Checks if tweet is original """
    try:
        return not bool(tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_IS_RETWEET.value))
    except NoSuchElementException:
        return True

def get_tweet_datetime(tweet: WebElement):
    """ Get tweet timestamp and parse it into datetime object """
    time_element = tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_TIMESTAMP.value)
    time_value = time_element.get_attribute("data-time-ms")
    timestamp = int(time_value) / 1000
    return dt.fromtimestamp(timestamp)

def parse_stat_numbers(number):
    """ Parses tweet statistic numbers """
    if not number:
        return 0
    if number[-1] == "K":
        return int(float(number[0:-1]) * 1000)
    return int(number)


def process_twitter(driver: webdriver.Chrome, person_id: int, twitter_link: str) -> TwitterAccount:
    """ Collects data from twitter page """
    driver.get(twitter_link)
    name = driver.find_element_by_css_selector(TwitterPageSelectors.PROFILE_NAME.value).text
    account_name = driver.find_element_by_css_selector(TwitterPageSelectors.ACCOUNT_NAME.value).text
    location = driver.find_element_by_css_selector(TwitterPageSelectors.LOCATION.value).text
    description = driver.find_element_by_css_selector(TwitterPageSelectors.DESCRIPTION.value).text
    register_date = driver.find_element_by_css_selector(TwitterPageSelectors.REGISTER_DATE.value).text
    tweet_amount = driver.find_element_by_css_selector(TwitterPageSelectors.TWEET_AMOUNT.value).text
    subscriptions_amount = driver.find_element_by_css_selector(TwitterPageSelectors.SUBSCRIPTIONS_AMOUNT.value).text
    subscribers_amount = driver.find_element_by_css_selector(TwitterPageSelectors.SUBSCRIBERS_AMOUNT.value).text
    likes_amount = driver.find_element_by_css_selector(TwitterPageSelectors.PROFILE_LIKES_AMOUNT.value).text
    scroll_untill_end(driver)
    account = TwitterAccount(name=name, atName=account_name)
    account_details = TwitterAccountDetails(
        description=description,
        location=location,
        registerDate=register_date,
        amountTweets=int(tweet_amount),
        amountSubscriptions=int(subscriptions_amount),
        amountSubscribers=int(subscribers_amount),
        amountLikes=likes_amount)
    account.twitterAccountDetails = account_details
    tweets = []
    for tweet in driver.find_elements_by_css_selector(TwitterPageSelectors.TWEETS.value):
        text = tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_TEXT.value).text
        datetime_posted = get_tweet_datetime(tweet)
        is_original = check_if_retweet(tweet)
        comments_element = tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_AMOUNT_COMMENTS.value)
        retweets_element = tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_AMOUNT_RETWEETS.value)
        likes_element = tweet.find_element_by_css_selector(TwitterPageSelectors.TWEET_AMOUNT_LIKES.value)
        tweet_record = Tweet(
            text=text,
            datetime=datetime_posted,
            isOriginal=is_original,
            amountComments=parse_stat_numbers(comments_element.text),
            amountRetweets=parse_stat_numbers(retweets_element.text),
            amountLikes=parse_stat_numbers(likes_element.text))
        tweets.append(tweet_record)
    account.tweets = tweets
    return SocialMediaRecord(person_id, account)

# TO-DO
def pass_linkedIn_login():
    """ Bypass linkedIn login if present """

def process_linkedIn(driver: webdriver.Chrome, person_record: Person, linkedIn_link: str) -> LinkedInAccount:
    """ Collects data from linkedIn page """
    driver.get(linkedIn_link)


def process_xing(driver: webdriver.Chrome, person_record: Person, xing_link: str) -> XingAccount:
    """ Collects data from xing page """
    driver.get(xing_link)
