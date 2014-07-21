import random
import inspect
from operator import lt, gt
from itertools import ifilter, ifilterfalse
from functools import wraps

from toolz import compose
from toolz.curried import do, partial


append = lambda v, l: do(l.append)(v) and l

insert = lambda v, l: do(partial(l.insert, 0)(v)) and l

head = lambda l: l[0]

tail = lambda l: l[1:]

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

def split_by(predicate, iterable):
    return map(list, [
        ifilter(predicate, iterable),
        ifilterfalse(predicate, iterable)
    ])


def take_first(func, it):
    for i in it:
        if func(i):
            return i


def take_first_not(func, it):
    for i in it:
        if not func(i):
            return i


# functions on dicts

def merge(dict_, second_dict=None, **kwargs):
    """copy and merge"""
    temp = dict_.copy()
    if second_dict:
        temp.update(second_dict)
    temp.update(kwargs)
    return temp


# predicates

is_integer = lambda x: isinstance(x, int)

is_zero = lambda x: x == 0

is_none = lambda x: x is None

is_true = lambda x: x is True

is_false = lambda x: x is False


def apply_last(func, last):
    @wraps(func)
    def __inner(first):
        return func(first, last)
    return __inner


smaller = lambda x: apply_last(lt, x)
larger = lambda x: apply_last(gt, x)


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
