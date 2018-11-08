class Peekable(object):
    """Peekable but otherwise perfectly normal iterator"""

    def __init__(self, it):
        self.it = iter(it)
        self.peeked = None

    def __iter__(self):
        return self

    def peek(self):
        self.peeked = next(self.it)
        return self.peeked

    def next(self):
        if self.peeked:
            value = self.peeked
            self.peeked = None
            return value
        else: 
            return next(self.it)

    __next__ = next


if __name__ == '__main__':
    p = Peekable(range(10))
    assert next(p) == 0
    assert next(p) == 1
    assert p.peek() == 2
    assert next(p) == 2
