""" Browser imperative code implementation """





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

# TO-DO
def pass_linkedIn_login():
    """ Bypass linkedIn login if present """

def process_linkedIn(driver: webdriver.Chrome, person_record: Person, linkedIn_link: str) -> LinkedInAccount:
    """ Collects data from linkedIn page """
    driver.get(linkedIn_link)


def process_xing(driver: webdriver.Chrome, person_record: Person, xing_link: str) -> XingAccount:
    """ Collects data from xing page """
    driver.get(xing_link)
