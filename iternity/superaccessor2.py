"""
Extremely experiemental, bound to give some people the creeps.

Another take on the whole superaccessor thing.

TODO: try to implement [] as an alias for map() a la jq

"""


def superget(obj, keystr):
    """
    >>> foos = [{'a': [1, 2, 3], 'b': [4, 5, 6]},
    ... {'a': ['x', 'y', 'z'], 'b': [999, 888, 777]},
    ... {'a': 'foo', 'b': '---'}]

    >>> superget(foos, "[0]['a'][2]")
    3
    >>> superget(foos, "[1]['b'][0]")
    999

    """
    return eval('obj' + keystr)


def superloop(iterator, keystr):
    """
    >>> foos = [{'a': [1, 2, 3], 'b': [4, 5, 6]},
    ... {'a': ['x', 'y', 'z'], 'b': [999, 888, 777]},
    ... {'a': 'foo', 'b': '---'}]

    >>> list(superloop(foos, "['a'][0]"))
    [1, 'x', 'f']

    """
    for item in iterator:
        yield eval('item' + keystr)
