import sys
from contextlib import contextmanager
from StringIO import StringIO


@contextmanager
def capture():
    """
    Context manager to capture stdout:

    >>> with capture() as captured:
    ...     print "hello"
    >>> print captured.getvalue()
    "hello"
    """
    temp = StringIO()
    sys.stdout = temp
    yield temp
    sys.stdout = sys.__stdout__


@contextmanager
def tap(obj):
    """
    Looks a bit weird but this is a bit like with statements work in
    some other languages (and a bit like ruby's tap, from where I
    stole the name), it simply saves a bit of typing.

    Example, assume you want to set

    long_object_name.long_attribute_name.foo = 10
    long_object_name.long_attribute_name.bar = 20
    long_object_name.long_attribute_name.baz = 30

    You could:

    with tab(long_object_name.long_attribute_name) as obj:
        obj.foo = 10
        obj.bar = 20
        obj.baz = 30

    """
    yield obj


@contextmanager
def suppress(*exceptions):
    """Context manager for suppressing certain exceptions.

    For python3, there's an identical context manager included as a part of
    functools.
    """
    try:
        yield
    except exceptions:
        pass
