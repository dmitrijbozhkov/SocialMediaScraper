""" Setup account identification application """
from collections import namedtuple
from social_media_scraper.identification.external_resources import read_csv, write_csv, throttle_emissions, prepare_browsers
from social_media_scraper.identification.process_search import identity_matcher

def run_app(args: dict):
    """
    Runs account identification application with passed arguments
    :param args: console arguments
    """
    reader = read_csv(args.input, True)
    writer = write_csv(args.output, ["Name", "LinkedIn", "Xing"])
    browsers = prepare_browsers(args.headless, args.geckodriver)
    matcher = identity_matcher(browsers)
    throttled_matcher = throttle_emissions(matcher, args.lower_bound, args.upper_bound)
    next(throttled_matcher)
    next(writer)
    for keywords in reader:
        matched = throttled_matcher.send(keywords)
        writer.send([keywords[0], matched.linked_in, matched.xing])
    throttled_matcher.close()
    writer.close()
