from functools import wraps
from inspect import isfunction


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


if __name__ == '__main__':
    def foo():
        pass
    decorated_foo = identity(foo)
    assert foo == undecorate(decorated_foo)
