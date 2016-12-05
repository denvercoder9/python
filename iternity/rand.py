import random


def coinflip():
    """Function representation a 50/50 chance of something happening"""
    return random.random > 0.5


def choicev(*items):
    """Variadic versions of random.choice"""
    return random.choice(items)


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
