"""
The rationale behind a lot of the functions in this module is that
many list functions return None. Having them return the list after
the modification instead allows for more brevity.

"""

import random
from itertools import islice, chain


def append(value, list_):
    """Append value to list and return the list"""
    list_.append(value)
    return list_


def insert(value, list_, position=0):
    """Insert value into list (default position is at the head) and return
    the list"""
    list_.insert(position, value)
    return list_


def extend(first, second):
    """Extends the first list with the second, syntactically a bit dangerous
    because it's the reverse of the other functions in this module. Consider
    using itertools.chain instead"""
    first.extend(second)
    return first


def sort(list_, **kwargs):
    """Sort the list and return it"""
    list_.sort(**kwargs)
    return list_


def shuffle(list_, **kwargs):
    """Shuffle the list and return it"""
    random.shuffle(list_, **kwargs)
    return list_


def shuffled(list_, **kwargs):
    """Return a shuffled list iterator, does not change the original list
    (similar to sorted())"""
    return iter(shuffle(list_[:], **kwargs))


#
# Various ways of consuming a list
#

def take(n, iterable):
    return islice(iterable, n)


#
# safe functional style accessors for lists (i.e don't raise key errors)
#

def _index_safe(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except IndexError:
        return None


def head(list_):
    """Return the first element of a list"""
    return _index_safe(lambda: list_[0])


def tail(list_):
    """Return everything but the first element of a list"""
    return _index_safe(lambda: list_[1:])


def last(list_):
    """Return the last element of a list"""
    return _index_safe(lambda: list_[-1])


def get(list_, index, default=None):
    """Safe get similar to dict.get, returns None or a given default value"""
    return _index_safe(lambda: list_[index]) or default


#
# Miscellaenous operations on lists
#


def flattened(iterable):
    """Flatten an iterator recursively"""
    for item in iterable:
        if hasattr(item, '__iter__'):
            for i in flattened(item):
                yield i
        else:
            yield item


def flatten(iterable):
    """Flatten and return a list"""
    iterable = list(flattened(iterable))
    return iterable


def compact(iterable):
    """Removed None values from list"""
    return filter(None, iterable)


def partition(iterable, n):
    """Partition list in chunks of size n, only whole chunks considered"""
    return zip(*[iter(iterable)] * n)


def partition_fill(iterable, n, filler=None):
    """Partitions list in chunks of size n, and adds fillter to the end"""
    if not len(iterable) == n:
        number_missing = n - len(iterable) % n
    return partition(chain(iterable, [filler]*number_missing), n)


if __name__ == '__main__':
    flat = [1, 2, 3, 4, 5]
    assert list(flattened([1, 2, 3, 4, 5])) == flat
    assert list(flattened([1, [2, 3], 4, 5])) == flat
    assert list(flattened([1, [2, [3]], [4, 5]])) == flat
    assert list(flattened([[1, [2, [3]], [4, 5]]])) == flat
    assert list(flattened([[[[[[1], [2], 3, 4]]], 5]])) == flat
    assert flatten([[1, 2, [3, [4], 5]]]) == flat
