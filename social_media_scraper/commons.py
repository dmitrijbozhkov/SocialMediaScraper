""" Common code accross program """
import re
import random
from rx import Observable, Observer
from cssselect import GenericTranslator

TS = GenericTranslator()

def fluctuate(left, right):
    """ Generates random floating point number within a range """
    while True:
        yield random.uniform(left, right)

def throttle_random(stream: Observable, left, right):
    """ Throttles requests, so that they come randomly in an interval """
    throttle = Observable \
        .from_(fluctuate(left, right)) \
        .concat_map(lambda a: Observable.just(a).delay(a * 1000))
    return Observable \
        .zip(stream, throttle, lambda e, f: e)

def throttle_filtered(stream: Observable, item: str, left, right):
    """ Throttles filtered items """
    filtered = stream \
        .filter(lambda r: r.get(item))
    return throttle_random(filtered, left, right)

def to_xpath(selector: str) -> str:
    """ Returns css selector for lxml """
    return TS.css_to_xpath(selector)

def extract_number(string: str) -> str:
    """ Searches for first number in string """
    return re.search(r"[-+]?\d*\.\d+|\d+", string).group()

def run_concurrently(stream: Observable, observer: Observer, tkinter_scheduler, pool_scheduler):
    """ Subscribe and apply scedulers """
    return stream \
        .observe_on(tkinter_scheduler) \
        .subscribe_on(pool_scheduler) \
        .subscribe(observer)