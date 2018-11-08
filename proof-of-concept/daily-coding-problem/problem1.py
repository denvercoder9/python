from itertools import combinations, starmap
import operator as op



def main(numbers, k):
    """
    Given a list of numbers and a number k, return whether any two numbers 
    from the list add up to k.

    For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 
    17.
    """
    return k in starmap(op.add, combinations(numbers, r=2))


if __name__ == '__main__':
    numbers = [10, 15, 3, 7]
    k = 17
    assert main(numbers, k)
