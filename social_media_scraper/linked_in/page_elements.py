""" LinkedIn page element constants """
from social_media_scraper.account.page_utils import to_xpath

# LinkedIn user info page selectors
NAME_LOCATION_SELECTOR = to_xpath("ul.pv-top-card--list > li:first-child")
CURRENT_POSITION = to_xpath(".mt2 h2")
EXPERIENCE_RECORD = to_xpath(".pv-position-entity")
EDUCATION_RECORD = to_xpath(".pv-education-entity")
EXPERIENCE_POSITION = to_xpath(".pv-entity__summary-info h3")
EXPERIENCE_COMPANY = to_xpath(".pv-entity__summary-info span.pv-entity__secondary-title")
EXPERIENCE_DATERANGE = to_xpath(".pv-entity__summary-info .pv-entity__date-range :nth-child(2)")
EXPERIENCE_DURATION = to_xpath(".pv-entity__summary-info span.pv-entity__bullet-item-v2")
EXPERIENCE_LOCATION = to_xpath(".pv-entity__summary-info .pv-entity__location :nth-child(2)")
EXPERIENCE_DESCRIPTION = to_xpath(".pv-entity__description")
EXPERIENCE_INNER_TIMELINE = to_xpath(".pv-entity__role-details-container")
TIMELINE_COMPANY = to_xpath(".pv-entity__company-summary-info h3 :nth-child(2)")
TIMELINE_POSITION = to_xpath(".pv-entity__summary-info-v2 h3 span:nth-child(2)")
TIMELINE_DATERANGE = to_xpath(".pv-entity__summary-info-v2 .pv-entity__date-range :nth-child(2)")
TIMELINE_DURATION = to_xpath(".pv-entity__summary-info-v2 span.pv-entity__bullet-item-v2")
TIMELINE_LOCATION = to_xpath(".pv-entity__summary-info-v2 .pv-entity__location :nth-child(2)")
TIMELINE_DESCRIPTION = to_xpath(".lt-line-clamp__line")
EDUCATION_FACILITY = to_xpath(".pv-entity__degree-info h3")
EDUCATION_SPECIALTY = to_xpath(".pv-entity__degree-info .pv-entity__fos span:nth-child(2)")
EDUCATION_DEGREE = to_xpath(".pv-entity__degree-info .pv-entity__degree-name span:nth-child(2)")
EDUCATION_DATERANGE = to_xpath(".pv-entity__dates span:nth-child(2)")
# Selectors for preparation
EDUCATION_ELEMENT = "#education-section"
EXPERIENCE_ELEMENT = "#experience-section"
MORE_LOCATOR = ".pv-profile-section__see-more-inline"
LESS_LOCATOR = ".pv-profile-section__see-less-inline"
EXPERIENCE_SECTION = ".pv-experience-section__see-more"
EDUCATION_SECTION = ".education-section .pv-profile-section__actions-inline"
COMPANY_TIMELINE_BUTTONS = ".pv-entity__paging"
BUTTON_MORE = ".pv-position-entity .lt-line-clamp__more"
CONTENT = ".pv-content"
# Search result elements
SEARCH_RESULT_LINKS = "li.search-result div.search-result__info a"
EMPTY_RESULTS = ".search-no-results__container"
