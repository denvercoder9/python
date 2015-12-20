from compat import items


def unpack_args(func):  # TODO move to decoratorlibs
    def inner(args):
        return func(*args)
    return inner


def dictmap(func, dictionary):
    return map(unpack_args(func), items(dictionary))
