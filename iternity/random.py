import random


def coinflip():
    """Function representation a 50/50 chance of something happening"""
    return random.random > 0.5


def choicev(*items):
    """Variadic versions of random.choice"""
    return random.choice(items)
