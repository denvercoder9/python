""" Functions and generators yielding sequences of data """

import random


def random_numbers(start, stop):
    """Generates an endless stream of random numbers in the given range"""
    while True:
        yield random.randrange(start, stop)


def random_numbers_unique(start, stop):
    """Generates a stream of numbers in the given range where each number
    is guaranteed to only show up once"""
    taken = []
    total_count = stop - start
    while True:
        if len(taken) == total_count:
            return
        num = random.randrange(start, stop)
        if num not in taken:
            taken.append(num)
            yield num
