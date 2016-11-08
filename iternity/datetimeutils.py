def copy_datetime(dt, **kwargs):
    """ Datetime objects can be a bit clumsy since they're not mutable.

    This copies a datetime object with the option to overwrite some values.
    """
    attrs = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    values = dict({attr: getattr(dt, attr, None) for attr in attrs}, **kwargs)
    return datetime(**values)
