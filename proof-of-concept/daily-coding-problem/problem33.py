"""
This problem was asked by Microsoft.

Compute the running median of a sequence of numbers. That is, given a stream 
of numbers, print out the median of the list so far on each new element.

Recall that the median of an even-numbered list is the average of the two middle numbers.

For example, given the sequence [2, 1, 5, 7, 2, 0, 5], your algorithm should print out:

2
1.5
2
3.5
2
2
2

"""

import bisect

def median(lst):
    medians = []
    for item in lst:
        bisect.insort(medians, item)
        if len(medians) == 1:
            yield item
        else:
            l, is_odd = divmod(len(medians), 2)
            if is_odd:
                yield medians[l]
            else:
                yield sum(medians[l-1:l+1]) / 2.0


assert list(median([2, 1, 5, 7, 2, 0, 5])) == [2, 1.5, 2, 3.5, 2, 2, 2]
