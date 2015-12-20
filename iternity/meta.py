"""Miscellaneous introspection and meta programming utilities.

Use at your own risk."""

from types import MethodType


def bind_method(obj, name, function):
    """Binds a method to a class instance.

    This solves the error when monkey patching a method on an instance,
    that self will not get properly bound"""
    setattr(obj, name, MethodType(function, obj))


def unbind_method(method):
    """Does the opposite of bind_method, extracts a method from a class
    so that it (depending on the method of course) can be used as a normal
    function"""
    return method.im_func
