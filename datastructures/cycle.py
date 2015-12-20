from itertools import islice


class Cycle(object):
    """This object is similar to itertools.slice but with is subscriptable
    and sliceable.
    """

    def __init__(self, seq):
        self.seq = seq
        self.length = len(self.seq)
        self._current = 0

    def __iter__(self):
        while True:
            current = self.seq[self._current]
            self._current = (self._current + 1) % self.length
            yield current

    def __getitem__(self, i):
        if isinstance(i, slice):
            return islice(self, i.start, i.stop, i.step)

        return self.seq[i % self.length]


def run_tests():
    test_cycle = lambda: Cycle([1, 2, 3, 4, 5])

    cycle = test_cycle()
    assert cycle[0] == 1
    assert cycle[1] == 2
    assert cycle[2] == 3
    assert cycle[3] == 4
    assert cycle[4] == 5
    assert cycle[5] == 1
    assert cycle[6] == 2
    assert cycle[7] == 3

    assert list(islice(test_cycle(), 0)) == []
    assert list(islice(test_cycle(), 10)) == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    assert list(islice(test_cycle(), 13)) == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5,
                                              1, 2, 3]
    assert list(islice(test_cycle(), 7)) == [1, 2, 3, 4, 5, 1, 2]

    assert list(test_cycle()[0:10]) == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    assert list(test_cycle()[0:20]) == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3,
                                        4, 5, 1, 2, 3, 4, 5]


if __name__ == '__main__':
    run_tests()
