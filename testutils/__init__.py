from mock import MagicMock as _MagicMock
from dateutil.parser import parse


def MagicMock(*args, **kwargs):
    """

    Should you pass a function to a decorator that tries to wrap it,
    use this function.

    A note on testing decorators: Don't overwrite the name of the original
    mock, as in:

    m = MagicMock()
    m = decorator(m)

    Because what you're getting back is not your mock (you get the "inner"
    function) and thus you can't use assert_called_with and similar
    methods. Use a new name and use the old name for assertions:

    m = MagicMock()
    decorated_m = decorator(m)
    decorated_m('foo')
    m.assert_called_with('foo')

    """
    defaults = {
        '__name__': 'MagicMock',
    }
    defaults.update(kwargs)
    return _MagicMock(*args, **defaults)


def datetime_almost_equals(datetime1, datetime2, precision='second',
                           tolerance=0):
    """
    Utility function to compare two datetime objects to desired precision.

    With microsecond precision this is the same as comparing two
    datetime objects directly.
    """
    if isinstance(datetime1, basestring):
        datetime1 = parse(datetime1)
    if isinstance(datetime2, basestring):
        datetime2 = parse(datetime2)

    attributes = [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'microsecond',
    ]
    for attr in attributes:
        if attr == precision:
            diff = abs(getattr(datetime1, attr) - getattr(datetime2, attr))
            return diff <= tolerance                       
        elif getattr(datetime1, attr) != getattr(datetime2, attr):
            return False


class MockChain(object):
    """
    Pretty much a chain of mock calls that ignores everything up til the
    interesting parts (no more foo.return_value.bar.return_value etc).

    Differentiates between function calls and attribute access by
    providing an alternative constructor for each:

    >>> from poplibs.dblib.models import Order
    >>> db = MockChain.method(count=10)
    >>> count = db.query(Order).filter(Order.id.in_(range(10))).count()
    >>> count
    10

    >>> foo = MockChain.attribute(calls=42)
    >>> foo.very
    <MockChain [very]>
    >>> foo.reset()
    >>> foo.very.long
    <MockChain [very, long]>
    >>> foo.reset()
    >>> foo.very.long.chain
    <MockChain [very, long, chain]>
    >>> foo.reset()
    >>> foo.very.long.chain.of.calls
    42
    """
    METHOD = 1
    ATTRIBUTE = 2

    def __init__(self, mode, **kwargs):
        self.mode = mode
        self.kwargs = kwargs
        self.call_trail = []

    def __getattr__(self, key):
        if key in self.kwargs and self.mode == self.ATTRIBUTE:
            return self.kwargs[key]
        else:
            self.call_trail.append(key)
            return self

    def __call__(self, *args, **kwargs):
        key = self.call_trail[-1]
        if key in self.kwargs:
            return self.kwargs[key]
        else:
            self.call_trail.append(key)
            return self

    def __nonzero__(self):
        return False

    @classmethod
    def method(cls, **kwargs):
        return cls(cls.METHOD, **kwargs)

    @classmethod
    def attribute(cls, **kwargs):
        return cls(cls.ATTRIBUTE, **kwargs)

    def __repr__(self):
        return '<MockChain [{}]>'.format(', '.join(self.call_trail))

    def reset(self):
        self.call_trail = []
