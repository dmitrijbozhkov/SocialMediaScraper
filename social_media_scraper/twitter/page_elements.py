""" Twitter page element costants """
from social_media_scraper.commons import to_xpath

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
# Twitter search elements
EMPTY_RESULTS = "div.SearchEmptyTimeline"
SEARCH_RESULT_LINKS = "div.ProfileCard > a"
