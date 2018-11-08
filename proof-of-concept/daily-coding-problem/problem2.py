"""
This problem was asked by Uber.

Given an array of integers, return a new array such that each element at index 
i of the new array is the product of all the numbers in the original array 
except the one at i.

For example, if our input was [1, 2, 3, 4, 5], the expected output would be
[120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be 
[2, 3, 6].

Follow-up: what if you can't use division?

"""

import operator as op


def with_division(numbers):
    total = reduce(op.mul, numbers)
    return [total / i for i in numbers]


def without_division(numbers):
    return [reduce(op.mul, numbers[:i] + numbers[i+1:]) for i, _ in enumerate(numbers)]


if __name__ == '__main__':
    data1 = [1, 2, 3, 4, 5]
    result1 = [120, 60, 40, 30, 24]

    data2 = [3,2,1]
    result2 = [2, 3, 6] 

    assert with_division(data1) == result1
    assert with_division(data2) == result2
    assert without_division(data1) == result1
    assert without_division(data2) == result2
