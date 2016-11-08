"""
Experimental module to fascilitate using python operators as partials.

functools.partial isn't enough in this case since most of the time
you want to provide the first argument (which is generally the object
being acted upon) last.

A mnemonic is that the arguments you provide first is the ones you'd
use to name the partial function:

    >>> add5 = partialop.add(5)
    >>> add5(10)
    15

In the case of operator.add, functools.partial would've been enough
since it's commutative, but most operators aren't:

    >>> sub5 = partialop.sub(5)
    >>> sub5(10)
    5

Using normal functools.partial in this case would've reversed the
meaning, i.e would've subtracted 10 from 5.

A lot fo these functions you'll likely never use, but a few of
them can be very helpful in a more functional programming style:

    >>> from partialop import lt
    >>> filter(lt(5), range(10)
    [0,1,2,3,4]

which, depending on whether you like this style of programming or
not, is infinitely more legible than:

    >>> filter(lambda x: x < 5, range(10))
    [0,1,2,3,4]
"""

import operator as op


def partial_right(f):
    return lambda *rhs: lambda lhs: f(lhs, *rhs)


# unary operators, partial doesn't make sense - include for completeness

unary = [
    'abs',
    'attrgetter',
    'isCallable',
    'isMappingType',
    'isNumberType',
    'isSequenceType',
    'itemgetter',
    'methodcaller',
    'neg',
    'not_',
    'pos',
    'truth'
]

for name in dir(op):
    f = getattr(op, name)
    globals()[name] = f if name in unary else partial_right(f)
