"""

This problem was asked by Google.

The power set of a set is the set of all its subsets. Write a function that, 
given a set, generates its power set.

For example, given the set {1, 2, 3}, it should return {{}, {1}, {2}, {3}, {1, 
2}, {1, 3}, {2, 3}, {1, 2, 3}}.

You may also use a list or array to represent a set.

"""

from itertools import chain, combinations


def powerset(s):
    ps = chain.from_iterable(combinations(s, r=i) for i in range(len(s) +1))
    return set(map(frozenset, ps))


def powerset(s):  # is this cleaner? I'm sure sure...
    ps = chain.from_iterable(combinations(s, r=i) for i, _ in enumerate(s, 1))
    return set(map(frozenset, ps)) | {frozenset()}



assert powerset({1, 2, 3}) == {
    frozenset({}),
    frozenset({1}),
    frozenset({2}),
    frozenset({3}),
    frozenset({1, 2}),
    frozenset({1, 3}),
    frozenset({2, 3}),
    frozenset({1, 2, 3})}, powerset({1,2,3})
