""" Manage input file """
from collections import namedtuple
import csv
from rx import Observable

PersonRecord = namedtuple("PersonRecord", ["person", "twitter", "linkedIn", "xing"])

def read_input(filename: str) -> PersonRecord:
    """ Reads input csv file and returns observable """
    file = open(filename)
    records = Observable.defer(lambda: Observable.from_(csv.reader(file))) \
        .skip(1) \
        .map(lambda r: PersonRecord(r[0], r[1], r[2], r[3]))
    return (file, records)
