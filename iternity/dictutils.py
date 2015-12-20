"""Some convenience functions for dicts"""


def pop(dict_, key, default=None):
    """Safe version of pop that returns a default if the key is non-existant"""
    return dict_.pop(key, default)


def delete(dict_, key):
    """Safe version of delete that does nothing if the key is non-existant"""
    if key in dict_:
        dict_.delete(key)


def update(dict_, *args, **kwargs):
    """Updates the dict and returns it"""
    dict_.update(*args, **kwargs)
    return dict_


def exlude(dict_, keys):
    """Return a dict minus the keys passed to the function"""
    new_dict = dict_.copy()
    for key in keys:
        pop(new_dict, key)
    return new_dict


def merge(dict_, *dicts, **kwargs):
    """Merge a dictionary with any number of other dictionary, plus keyword
    arguments.

    Any key that already exists will be overwritten if it's present in later
    dicts as well.
    """
    new_dict = dict_.copy()
    for d in dicts:
        new_dict.update(d)
    new_dict.update(kwargs)
    return new_dict
