from functools import wraps
from inspect import isfunction
try:
    import ipdb as debugger
except ImportError:
    import pdb as debugger


def identity(f):
    """The identify decorator - does nothing"""
    @wraps(f)
    def inner(*args, **kwargs):
        return f(*args, **kwargs)
    return inner


def undecorate(f):
    """Tries to extract the original undecorated function"""
    if not f.__closure__:
        return
    for cell in f.__closure__:
        temp = cell.cell_contents
        if isfunction(temp):
            return temp


def cachedproperty(method):
    @wraps(method)
    def inner(self):
        if not hasattr(self, '_cache'):
            self._cache = {}
        if method.__name__ not in self._cache:
            self._cache[method.__name__] = method(self)

        return self._cache[method.__name__]
    return property(inner)


def pdb(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            debugger.set_trace()
    return inner


def as_list(f):
    """Automatically exhaust a generator.

    Wrap your generator function in this when you want to use the neater
    generator syntax while still returning a normal list instead of a
    generator.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        return list(f(*args, **kwargs))
    return inner


if __name__ == '__main__':
    # test undecorate

    def foo():
        pass
    decorated_foo = identity(foo)
    assert foo == undecorate(decorated_foo)

    # test cachedproperty

    from time import sleep

    class X(object):
        @cachedproperty
        def foo(self):
            sleep(4)  # simulating CPU intensive operation
            return "foo"

    x = X()
    print x.foo
    print x.foo
