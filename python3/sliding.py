"""
Different implementation of sliding window functions.

"""


from collections import deque
from itertools import islice, tee


def sliding_window(data, size):
    data = iter(data)
    first, *rest = islice(data, size)
    yield tuple((first, *rest))

    while True:
        first, *rest = rest
        rest.append(next(data))

        yield tuple((first, *rest))


def sliding_window2(data, size):
    data = iter(data)
    rest = islice(data, size)
    while True:
        first, *rest = rest
        yield tuple((first, *rest))
        rest.append(next(data))


def sliding_window3(data, size):
    data = iter(data)
    rest = deque(islice(data, size), size)
    while True:
        yield tuple(rest)
        rest.append(next(data))


def sliding_window4(data, size):
    its = tee(data, size)
    for i, iterator in enumerate(its):
        list(islice(iterator, i))   # the list call is important, you need to consume!
    yield from zip(*its)


data = range(10)
print(list(sliding_window(data, 3)))
print(list(sliding_window2(data, 3)))
print(list(sliding_window3(data, 3)))
print(list(sliding_window4(data, 3)))
