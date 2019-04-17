""" Common scripts, shared between different websites """

CHOOSE_ELEMENT = r"""<div id="choose-prompt" style="position: fixed; background-color: blue; color: white; text-align: center; width: 100%; height: 40px; z-index: 9999999999; font-size: 18px;">Please click on account to choose it</div>"""
ELEMENT_CHOSEN = r"""<div id="chosen-prompt" style="display:none;position: fixed;background-color: grey;width: 100%;height: 100%;color: white;z-index: 9999999999;text-align: center;vertical-align: middle;display: flex;align-items: center;justify-content: center;font-size: 3em;background-color: rgba(46, 49, 49, 0.8);">Account chosen, waiting for other to finish</div>"""
CHOSEN_LINK_CLASS = ".chosen-link-selenium"

SET_DONE = r"""
function setDone() {
    document.body.insertAdjacentHTML("afterbegin", '""" + ELEMENT_CHOSEN + r"""');
    document.querySelector("div#chosen-prompt").style.display = "block";
}
"""

def build_script(selector: str) -> str:
    """ Makes skript, that manages search results """
    return r"""
    """+ SET_DONE + r"""
    let foundLinks = document.querySelectorAll('""" + selector + r"""');
    if (foundLinks.length === 0) {
        setDone();
        return 0;
    }
    if (foundLinks.length > 2) {
        document.body.insertAdjacentHTML("afterbegin", '""" + CHOOSE_ELEMENT + r"""');
        return null;
    }
    setDone();
    return foundLinks[0].href;
    """
