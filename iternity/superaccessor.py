"""
Experimental module for access to keys, items and methods.

How often have we not done stuff like:

>>> map(lambda x: x['somekey'], listofdicts)

This is a bit unwieldy. You can get it a bit more succint if you're
using the operators module:

>>> import operator as op
>>> map(op.itemgetter('somekey'), listofdicts)

But if you're lazy like me, that's still a bit too much to type.
The SuperAccessor object (conveniently aliased to _, but watch out when
playing around with it in the REPL) offers a more succint way of doing
this, as well as getting attributes and calling methods on objects:

>>> map(_['somekey'], listofdicts)
>>> map(_.someattr, listofobjects)
>>> map(_.somemethod, listofobjects)

"""


import operator as op

class SuperAccessor(object):
    def __getattr__(self, name):
        return op.attrgetter(name)

    def __getitem__(self, name):
        return op.itemgetter(name)

    def __call__(self, name, *args, **kwargs):
        return op.methodcaller(name, *args, **kwargs)

_ = SuperAccessor()


if __name__ == '__main__':
    itemtest = [
        {'foo': 99, 'bar': 100}, {'foo': 567, 'bar': 999}, {'foo': 123, 'bar': 345}
    ]
    assert map(_['foo'], itemtest) == [99, 567, 123]

    class TestClass(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def z(self):
            return self.x + self.y

        def add_to_z(self, i):
            return self.z() + i

    testdata = [TestClass(10, 5), TestClass(4, 3), TestClass(1, 19)]

    assert map(_.x, testdata) == [10, 4, 1]
    assert map(_('z'), testdata) == [15, 7, 20]
    assert map(_('add_to_z', 10), testdata) == [25, 17, 30]
