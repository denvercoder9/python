# *-* coding: utf-8

"""
This problem was asked by Google.

The area of a circle is defined as πr^2. Estimate π to 3 decimal places using 
a Monte Carlo method.

Hint: The basic equation of a circle is x2 + y2 = r2.


From wikipedia:

For example, consider a quadrant inscribed in a unit square. Given that 
the ratio of their areas is π/4, the value of π can be approximated using a 
Monte Carlo method:[11]

* Draw a square, then inscribe a quadrant within it
* Uniformly scatter a given number of points over the square
* Count the number of points inside the quadrant, i.e. having a distance from 
  the origin of less than 1
* The ratio of the inside-count and the total-sample-count is an estimate of 
  the ratio of the two areas, π/4. Multiply the result by 4 to estimate π.

"""

from math import sqrt
from random import random


def random_point():
	return (random(), random())


def is_inside((x, y)):
    return sqrt(x ** 2 + y ** 2) <= 1


def monte_carlo():
    n_inside = 0
    n = 0
    max_n = 20000000

    while True:
        n += 1
        n_inside += bool(is_inside(random_point()))
        
        if n > max_n:
            break

    return n_inside / float(n) * 4


print monte_carlo()
