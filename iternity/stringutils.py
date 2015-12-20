def join(char, iterable):
    """Joins all kinds of iterables with char. All items are automatically
    converted to strings.

    >>> join(', ', range(10))
    '0, 1, 2, 3, 4, 5, 6, 7, 8, 9'
    """
    return char.join(map(str, iterable))


def joinv(char, *items):
    """Variadic version of join

    >>> join('-', 1, 2, 3)
    '1-2-3'
    """
    return join(char, items)
