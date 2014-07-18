import random
import inspect

from functools import wraps
from toolz.curried import do, partial


append = lambda v, l: do(l.append)(v) and l

insert = lambda v, l: do(partial(l.insert, 0)(v)) and l

tail = lambda l: l[1:]

sort = do(list.sort)

shuffle = do(random.shuffle)


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


def random_numbers(start, stop):
    while True:
        yield random.randint(start, stop)


### experimental ###


def numbers(start=0, step=1):
    number = start
    while True:
        yield number
        number += step


def take_first(func, it):
    for i in it:
        if func(i):
            return i


def take_first_not(func, it):
    for i in it:
        if not func(i):
            return i
