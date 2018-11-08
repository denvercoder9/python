def find_lowest_positive(lst):
    """This problem was asked by Stripe.

    Given an array of integers, find the first missing positive integer
    in linear time and constant space. In other words, find the lowest
    positive integer that does not exist in the array. The array can contain
    deuplicates and negative numbers as well.
    """
    i = 1
    while True:
        if i not in lst:
            return i

        i += 1


assert find_lowest_positive([3, 4, -1, 1]) == 2
assert find_lowest_positive([1, 2, 0]) == 3


# With external libs

from first import first
from itertools import count


def find_lowest_positive(lst):
    return first(i for i in count(1) if i not in lst)


assert find_lowest_positive([3, 4, -1, 1]) == 2
assert find_lowest_positive([1, 2, 0]) == 3


# With external libs, probably my favorite

def find_lowest_positive(lst):
    return first(count(1), key=lambda x: x not in lst)


assert find_lowest_positive([3, 4, -1, 1]) == 2
assert find_lowest_positive([1, 2, 0]) == 3


# Or even better but more verbose

def not_in(lst):
    return lambda item: item not in lst


def find_lowest_positive(lst):
    return first(count(1), key=not_in(lst))


assert find_lowest_positive([3, 4, -1, 1]) == 2
assert find_lowest_positive([1, 2, 0]) == 3
