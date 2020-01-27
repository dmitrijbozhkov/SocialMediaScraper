""" Page element constants """
from social_media_scraper.account.page_utils import to_xpath

# Xing profile selectors
NAME = to_xpath("h2[data-qa='malt-profile-display-name']")
CURRENT_POSITION = to_xpath("div[data-qa='profile-occupations'] p")
LOCATION = to_xpath("div[data-qa='profile-location'] p")
ENTRY_BOX = to_xpath("div[class*='bucket-bucket-odl-content']")
ENTRY_SELECTOR = to_xpath("button")
POSITION_SELECTOR = to_xpath("h3")
PLACE_SELECTOR = to_xpath("h3 + p")
EDUCATION_SUBJECT_SELECTOR = to_xpath("p[class*='entryOverview-entryOverview-description'] > span")
DATE_SELECTOR = to_xpath("div[class*='entryTime-entryTime-time'] > p")
HAVES = to_xpath("#haves li")
WANTS = to_xpath("#wants li")
# Xing page selector
OUTER_CONTENT = "html"
# JavaScript code to wait for
INNER_FRAME_READY = r"""
var frameElement = document.querySelector('iframe#tab-content');
if (frameElement) {
    if (frameElement.contentWindow.$) {
        if (frameElement.contentWindow.document.body) {
            return frameElement.contentWindow.$.active;
        }
    }
}
return 1;
"""
# Xing search selectors
NO_RESULTS_CONTAINER = "//div[contains(text(), 'No members found') and @data-qa='results-overview']"
SEARCH_RESULT_LINKS = "div[data-qa=\"results-list\"] > a"
