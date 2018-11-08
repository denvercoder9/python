"""
Just for funz: This is my favorite implementation of fizzbuzz. 

"""

from itertools import cycle, izip, islice


def fizzbuzz(n=10):
    fizz = cycle(['', '', 'Fizz'])
    buzz = cycle(['', '', '', '', 'Buzz'])

    for i, fizzbuzz in enumerate(islice(izip(fizz, buzz), n), 1):
        print ''.join(fizzbuzz) or i


if __name__ == '__main__':
    fizzbuzz(100)


# it's easy but not pretty to turn this into a one-liner (minus imports)

print [''.join(fizzbuzz) or i for i, fizzbuzz in enumerate(islice(izip(cycle(['', '', 'Fizz']), cycle(['', '', '', '', 'Buzz'])), 100), 1)]
