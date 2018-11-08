"""
The Collatz conjecture is a conjecture in mathematics that concerns a sequence
defined as follows: start with any positive integer n. Then each term is
obtained from the previous term as follows: if the previous term is even, the
next term is one half the previous term. Otherwise, the next term is 3 times
the previous term plus 1. The conjecture is that no matter what value of n,
the sequence will always reach 1.
"""

import sys


def collatz(n):
    while True:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1

        yield n


def main(n):
    for i, value in enumerate(collatz(n), start=1):
        print value
        if value == 1:
            return i


if __name__ == '__main__':
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        print 'We reached 1 in {} iterations'.format(main(n))
