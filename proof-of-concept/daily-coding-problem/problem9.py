"""
This problem was asked by Airbnb.

Given a list of integers, write a function that returns the largest sum of non-
adjacent numbers. Numbers can be 0 or negative.

For example, [2, 4, 6, 2, 5] should return 13, since we pick 2, 6, and 5.
[5, 1, 1, 5] should return 10, since we pick 5 and 5.

Follow-up: Can you do this in O(N) time and constant space?

"""


def sum_of_non_adjecent(data):
    incl = excl = 0
    for i in data:
        incl, excl = excl + i, max(excl, incl)
    return max(excl, incl)


assert sum_of_non_adjecent([2, 4, 6, 2, 5]) == 13
assert sum_of_non_adjecent([5, 1, 1, 5]) == 10
