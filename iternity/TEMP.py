"""
DISCLAIMER: THIS FILE TOTALLY UNORDERED AND NOT INTENDED FOR USE BY ANY MEANS AT ALL

SOME OF THE USEFUL STUFF WILL HOWEVER END UP IN THE OTHER MODULES, SOME WILL BE FOOD
FOR THOUGHT OR EXPERIMENTATION AND MOST WILL GET SCRAPPED
"""

import random
import inspect
import operator as op
from operator import lt, gt, contains
from itertools import ifilter, ifilterfalse, takewhile
from functools import wraps
from collections import OrderedDict
from compiler import ast
from toolz import compose, groupby
from toolz.curried import do, partial
from operator import itemgetter, attrgetter


# append = lambda v, l: _do(l.append, v) and l
# append = lambda v, l: l.append(v) or l

# insert = lambda v, l: _do(partial(l.insert, 0), v) and l
# insert = lambda v, l: l.insert(0, v) or l

# extend = partial(reduce, op.add)

# head = lambda l: l[0]           #  operator.itemgetter(0)

# tail = lambda l: l[1:]          #  operator.itemgetter(slice(1, None))

# last = lambda l: l[-1]          #  operator.itemgetter(-1)

# sort = do(list.sort)

# shuffle = do(random.shuffle)

# isort = compose(sort, iter)

# ishuffle = compose(shuffle, iter)


#  infinite sequences

def numbers(start=0, step=1):
    number = start
    while True:
        yield number
        number += step


# def random_numbers(start, stop):
#     while True:
#         yield random.randint(start, stop-1)


# def random_numbers_unique(start, stop):
#     taken = []
#     total_count = stop - start
#     while True:
#         if len(taken) == total_count
#             break
#         num = random.randrange(start, stop)
#         if num not in taken:
#             taken.append(num)
#             yield num


#  functions on lists

def drop(excludes, iterable):
    for item in iterable:
        if item not in excludes:
            yield item


# def get(list_, index, default=None):
#     """List equivalent of dict.get"""
#     try:
#         return list_[index]
#     except IndexError:
#         return default


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


def is_iterable(it):
    try:
        iter(it)
    except TypeError:
        return False
    else:
        return True


# partial operators

add = partial(reduce, op.add)

sub = partial(reduce, op.sub)

mul = partial(reduce, op.mul)

div = partial(reduce, op.div)


# recursive

# TODO recursive sub-namespace... for example recursive.reduce,
# recursive.map (?)


# boolean operators

none = lambda i: not any(i)

some = lambda i: not all(i)


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




def unique(iterable, keyfunc=None):
    """
    yield only items unique based on keyfunc, first occurence wins
    """
    keys = set()
    for item in iterable:
        key = keyfunc(item) if keyfunc else item
        if key not in keys:
            keys.add(key)
            yield item


def unique_last(iterable, keyfunc=None):
    """
    yield only items unique based on keyfunc, last occurence wins

    note that is way more wasteful than unique() since the whole dict
    has to be filled first
    """
    result = OrderedDict()
    for item in iterable:
        key = keyfunc(item) if keyfunc else item
        result[key] = item
    for key, item in result.iteritems():
        yield item


def split_on(predicate, iterable):
    """
    Return two lists: the first one for the items in `iterable`
    where `predicate` is true, the second one where it's false

    >>> less_than_5 = lambda x: x < 5
    >>> split_on(less_than_5, range(10))
    ([0, 1, 2, 3, 4], [5, 6, 7, 8, 9])
    """
    split = defaultdict(list)
    for item in iterable:
        split[predicate(item)].append(item)
    return split[True], split[False]


def split_by(predicate, iterable):
    return (
        chain.from_iterable(take_evens(toolz.partitionby(predicate, iterable))),
        chain.from_iterable(take_odds(toolz.partitionby(predicate, iterable)))
    )


# non-lazy
def take_nth(n, iterable, start=0):
    return toolz.take_nth(n, list(iterable)[start:])


# non-lazy
def take_odds(iterable):
    return take_nth(2, iterable, 1)


# non-lazy
def take_evens(iterable):
    return toolz.take_nth(2, iterable)


def group_by(func, iterable, predicate=None, transform=None):
    predicate = predicate or (lambda _: True)
    transform = transform or (lambda item: item)

    grouped = defaultdict(list)
    for item in iterable:
        if predicate(item):
            grouped[func(item)] = transform(item)
    return grouped


def flatten(list_):
    return ast.flatten(list_)


def unpack(func):
    def inner(*args):
        return func(*args)
    return inner


def umap(func, iterable):
    " unpacking version of map "
    return [func(*args) for args in iterable]


def unpack(callable):
    def inner(*args):
        return callable(*args[0])
    return inner


def pack(callable):
    def inner(*args):
        return callable(args)
    return inner


def format_object(obj):
    return ', '.join(['{}: {}'.format(k, v) for k, v in obj.__dict__.items()])


def first_true(pred, it):
    if pred(first(it)):
        return first(it)
    else:
        return first(dropwhile(lambda x: not pred(x)), it)


def first_false(pred, it):
    return first(dropwhile(pred, it))

"""
try_until could maybe be a dropwhile + first

first_true -> first(dropwhile( .... ))
"""


def ids(iterable):
    return [item.id for item in iterable]



def split(iterable, predicate):
    return filter(predicate, iterable), filter(lambda x: not predicate(x), iterable)


def filter_none(iterable):
  return filter(None, iterable)


def filter_false(iterable):
  return filter(false, iterable)


def filter_true(iterable):
  return filter(true, iterable)


class Getter(object):
    """Very experimental syntax for [] and .attr access in for example 
    map expressions. Likely to be very frowned upon ;)

    map(_[0], [(1,2), (3,4), (5,6)])
    map(_.foo, [someobj1, someobj2, someobj3])
    """
    def __getitem__(self, name):
        return itemgetter(name)
    def __getattr__(self, name):
        return attrgetter(name)

_ = Getter()



def order_by(iterable, key):
    return sorted(iterable, key=key)


def length(iterable):
  return len(list(iterable))


def count_true(predicate, iterable):
    return len(filrer(predicate, iterable))


def groupby(iterable, key):
    """A more sane version of itertools.groupby"""
    groupby = itertools.groupby
    return [(key, list(values)) for key, values in groupby(sorted(iterable, key=key), key)]


def format_object(obj):
    return ', '.join(['{}: {}'.format(k, v) for k, v in obj.__dict__.items()])


class TrueDict(dict):
    '''
    A dict that never sets key = None, that is
    you will never have to:
    
    if b:
        a['b'] = b

    '''
    def __setitem__(self, key, value):
        if value:
            dict.__setitem__(self, key, value)

    def set_none(self, key):
        setattr(self, key, None)


def filter(first, second=None):
    '''For those of us not really liking the filter(None, iterable) syntax'''
    
    if callable(first) and second:
        return __builtins__.filter(first, second)
    else:
        return __builtins__.filter(None, first)
