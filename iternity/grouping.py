"""Contains different functions for grouping data"""

from collections import defaultdict
from operators import itemgetter, attrgetter


def group_by(func, iterable):
    """Group some data by the return value of func

    >>> group_by(lambda x: x < 5, range(10))
    {False: [5, 6, 7, 8, 9], True: [0, 1, 2, 3, 4]}
    """
    grouped = defaultdict(list)
    for item in iterable:
        grouped[func(item)].append(iterable)
    return dict(grouped)


key = itemgetter

attr = attrgetter


def groupby_attr(name, it):
    """Group by attribute of an object """
    return group_by(attr(name), it)


def groupby_key(name, it):
    """Group by the key of an subscriptable object"""
    return group_by(key(name), it)


groupby_index = groupby_key


def ungroup(dict_):
    """yield key-value pairs from a dict where the values are lists,
    more or less a reverse groupby
    """
    for key, values in dict_.items():
        for value in values:
            yield key, value
