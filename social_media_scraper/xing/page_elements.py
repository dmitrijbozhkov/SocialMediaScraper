""" Page element constants """
from social_media_scraper.commons import to_xpath

# Xing profile selectors
NAME = to_xpath("h2[data-qa='malt-profile-display-name'] > span")
CURRENT_POSITION = to_xpath("div[data-qa='profile-occupations'] p")
LOCATION = to_xpath("div[data-qa='profile-location'] p")
WORK_EXPERIENCE = to_xpath("input#work-experience-data")
EDUCATION = to_xpath("input#education-data")
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
