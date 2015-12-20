"""
The functions in this module are predicate functions.

Use when filtering, sorting etc.
"""

from functools import wraps, partial
import operator as op
from types import ComplexType


def is_integer(value):
    """Returns true for integer and long, since this distinction often
    is meaningless"""
    return isinstance(value, int) or isinstance(value, long)


def is_float(value):
    """Returns true for floats"""
    return isinstance(value, float)


def is_complex(value):
    """Returns true for complex numbers"""
    return isinstance(value, ComplexType)


def is_number(value):
    """Returns true for integer, long, float and complex"""
    return is_integer(value) or is_float(value) or is_complex(value)


def is_even(value):
    """Returns true if value is an even number"""
    return value % 2 == 0


def is_odd(value):
    """Returns true if value is an odd number"""
    return value % 2 == 1


def is_zero(value):
    """Returns true if value is zero"""
    return value == 0


def is_none(value):
    """Returns true when value is None"""
    return value is None


def is_true(value):
    """Returns true when value is True"""
    return value is True


def is_itrue(value):
    """Returns to when value is True in a boolean context"""
    return bool(value) is True


def is_false(value):
    """Returns true when value is False"""
    return value is False


def is_ifalse(value):
    """Returns true when value is False in a boolean context"""
    return bool(value) is False


def is_iterable(value):
    """Returns true when value is iterable"""
    return getattr(value, '__iter__') or isinstance(value, basestring)


def is_property(instance, name):
    """Returns true a method is a property"""
    return isinstance(getattr(instance.__class__, name), property)


def apply_last(func, last):  # TODO move to decoratorlib
    """Returns a callable where 'last' is guaranteed to be called as last
    argument"""
    @wraps(func)
    def __inner(*args):
        args += (last, )
        return func(*args)
    return __inner


def greater_than(value):
    """Returns a predicate function that returns true for x > value

    >>> greater_than_five = greater_than(5)
    >>> filter(greater_than_five, range(10))
    [6,7,8,9]
    """
    return apply_last(op.gt, value)


def less_than(value):
    """Returns a predicate function that returns true for x < value

    >>> less_than_five = less_than(5)
    >>> filter(less_than_five, range(10))
    [0,1,2,3,4]
    """
    return apply_last(op.lt, value)

smaller_than = less_than  # alias


def in_(container):
    """Returns a predicate function that returns true if x in container

    >>> collection = [-1,7,9,12]
    >>> filter(in_(collection), range(10))
    [7, 9]
    """
    return partial(op.contains, container)


def inv(*container):
    """Variadic version of in_
    >>> filter(inv(-1,0,1), range(10))
    [0, 1]
    """
    return partial(op.contains, container)


def non_in(container):
    """Returns a predicate function that returns true if x not in container

    >>> collection = [-1,7,9,12]
    >>> filter(not_in(collection), range(10))
    [0, 1, 2, 3, 4, 5, 6, 8]
    """
    return lambda value: value not in container


def not_inv(*container):
    """Variadic version of not_in

    >>> filter(not_inv(-1,0,1), range(10))
    [2, 3, 4, 5, 6, 7, 8, 9]
    """
    return lambda value: value not in container
