"""

Disclaimer: 100% work in progress.

This is my personal attempt at creating a library to facilitate functinal
programming in python.


Personal todo-list:

* clump
    clump(n, iter)
    clump_all(n, iter, default=None)

    >> clump(3, range(10)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]

    >> clump_all(3, range(10))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]

* irand_int
* irand_int_unique
"""

import random
import inspect
import operator as op
from operator import lt, gt, contains
from itertools import ifilter, ifilterfalse, takewhile
from functools import wraps

from toolz import compose, groupby, do as _do
from toolz.curried import do, partial

append = lambda v, l: _do(l.append, v) and l

insert = lambda v, l: _do(partial(l.insert, 0), v) and l

extend = partial(reduce, op.add)

head = lambda l: l[0]           # operator.itemgetter(0)

tail = lambda l: l[1:]          # operator.itemgetter(slice(1, None))

last = lambda l: l[-1]          # operator.itemgetter(-1)

sort = do(list.sort)

shuffle = do(random.shuffle)

isort = compose(sort, iter)

ishuffle = compose(sort, iter)


# infinite sequences

def numbers(start=0, step=1):
    number = start
    while True:
        yield number
        number += step


def random_numbers(start, stop):
    while True:
        yield random.randint(start, stop)


# functions on lists

def get(list_, index, default=None):
    """List equivalent of dict.get"""
    try:
        return list_[index]
    except IndexError:
        return default


def split_by(predicate, iterable):
    return map(list, [
        ifilter(predicate, iterable),
        ifilterfalse(predicate, iterable)
    ])


def _take_first(func, it):
    for i in it:
        if func(i):
            yield i
            raise StopIteration


def take_first(func, it):
    return next(_take_first(func, it))


def _take_first_not(func, it):
    for i in it:
        if not func(i):
            yield i
            raise StopIteration


def take_first_not(func, it):
    return next(_take_first_not(func, it))


def filter_none(it):
    return filter(None, it)


def av_filter(list_of_objects, **kwargs):
    '''attribute->value filter

    >>> class A(object):
    ...    def __init__(self, x):
    ...       self.x = x
    >>> a = A(10)
    >>> b = A(11)
    >>> foo = [a, b]
    >>> res = list(av_filter(foo, x=10))
    >>> a in res
    True
    >>> b in res
    False
    >>> list(av_filter(foo, y=10))
    []
    '''
    k, v = kwargs.popitem()
    for obj in list_of_objects:
        try:
            if getattr(obj, k) == v:
                yield obj  # TODO return value or whole object?
        except AttributeError:
            pass


def kv_filter(list_of_dicts, **kwargs):
    '''key->value filter

    >>> foo = [{'a': 10, 'b': 11}, {'a': 99, 'c': 100}]
    >>> list(kv_filter(foo, a=10))
    [{'a': 10, 'b': 11}]
    >>> list(kv_filter(foo, d=99))
    []
    '''

    k, v = kwargs.popitem()
    for dict_ in list_of_dicts:
        try:
            if dict_[k] == v:
                yield dict_   # TODO return value or whole dict?
        except KeyError:
            pass


# grouping

def groupby_attr(attr, it):
    return groupby(op.attrgetter(attr), it)


def groupby_key(key, it):
    return groupby(op.itemgetter(key), it)


# or the above two "zum selbstbauen" (use as functions with vanilla groupby)

key = op.itemgetter

attr = op.attrgetter


# functions on dicts

def merge(dict_, second_dict=None, **kwargs):
    """copy and merge"""
    temp = dict_.copy()
    if second_dict:
        temp.update(second_dict)
    temp.update(kwargs)
    return temp


def dictmap(func, dict_):
    return [func(k, v) for k, v in dict_.iteritems()]


def exclude(dict_, keys):
    # TODO: is copy(dict_, exclude=None) a better semantic?
    new_dict = dict_.copy()
    for key in keys:
        new_dict.pop(key)
    return new_dict


# silent functions (don't raise exceptions)


def silent_map(function, iterable):
    temp = []
    for item in iterable:
        try:
            temp.append(function(item))
        except Exception:
            pass
    return temp

smap = silent_map


def silent_reduce(function, iterable, start=0):
    temp = start
    for item in iterable:
        try:
            temp = function(temp, item)
        except Exception:
            pass
    return temp

sreduce = silent_reduce


def silent_filter(function, iterable):
    temp = []
    for item in iterable:
        function = bool if function is None else function
        try:
            if function(item):
                temp.append(item)
        except Exception:
            pass
    return temp

sfilter = silent_filter


# predicates

def apply_last(func, last):
    @wraps(func)
    def __inner(first):
        return func(first, last)
    return __inner

is_integer = lambda x: isinstance(x, int)

is_zero = lambda x: x == 0

is_none = lambda x: x is None

is_itrue = lambda x: bool(x)    # is implicit true

is_true = lambda x: x is True

is_talse = lambda x: x is False

is_iterable = lambda x: isinstance(x, basestring) or '__iter__' in dir(x)

#def is_iterable(it):
#    try:
#        iter(it)
#    except TypeError:
#        return False
#    else:
#        return True

smaller = lambda x: apply_last(lt, x)

larger = lambda x: apply_last(gt, x)

in_ = lambda x: partial(contains, x)


# partial operators

add = partial(reduce, op.add)  # this is really nothing but a sum()?

sub = partial(reduce, op.sub)

mul = partial(reduce, op.mul)

div = partial(reduce, op.div)


# recursive

# TODO recursive sub-namespace... for example recursive.reduce,
# recursive.map (?)


# experimental

def insert_first(func):
    '''decorator to make first parameter not madatory'''
    @wraps(func)
    def __inner(*args, **kwargs):
        if len(inspect.getargspec(func).args) == len(args):
            args = list(args)
            first = args.pop()
            return func(first, *args, **kwargs)
        return func(*args, **kwargs)
    return __inner


@insert_first
def irandrange(stop, start=0):
    for _ in range(start, stop):
        yield random.randrange(start, stop)


@insert_first
def irandrange_unique(stop, start=0):
    for i in shuffle(range(start, stop)):
        yield i


@insert_first
def irandrange_exclude(stop, exclude, start=0):
    for i in irandrange(start, stop):
        if i not in exclude:
            yield i


def call_while(predicate, function, *args, **kwargs):
    result = None
    while predicate:
        result = function(*args, **kwargs)
    return result


def call_while_not(predicate, function, *args, **kwargs):
    result = None
    while not predicate:
        result = function(*args, **kwargs)
    return result


def get_longest_match(foo, bar):
    is_same = lambda tup: tup[0] == tup[1]
    return len(list(takewhile(is_same, zip(foo, bar))))
