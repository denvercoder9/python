"""Some very basic math going on here"""

from collections import Counter
from predicate import is_odd


def integer_sum(n):
    """Sum the first n integer values from zero a la Gauss

    This is likely to be completely useless most of the time but when
    summing large lists where the items are consecutive integers
    starting from zero, this is a lot faster"""
    return n * (n + 1) / 2


def average(list_):
    """Return the avage of a list"""
    return sum(list_) / float(len(list_))


def median(list_):
    """Return the median of a list, i.e the mid element of a list of uneven
    number of items, and the average of the two middle elements in a list of
    even number of items
    """
    count = len(list_)
    mid = count/2
    sorted_list = list(sorted(list_))
    if is_odd(count):
        return sorted_list[mid]
    else:
        return average([[sorted_list[mid], sorted_list[mid-1]])


def mode(list_):
    """Return the mode of the list, i.e. the item that show up most
    frequently in it"""
    return Counter(list_).most_common(1)[0][0]
