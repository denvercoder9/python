"""
I almost never use descriptors although they're a powerful tool.

An oft touted example of descriptors is @property

I wanted to see for myself whether this would be hard to implement
from scratch as a descriptor. Turned out it wasn't...

"""


class prop(object):
    def __init__(self, method):
        self.method = method
        self.obj = None

    def __get__(self, obj, type_):
        self.obj = obj
        return self.method(obj)

    def setter(self, method):
        self.setter_method = method
        return self

    def __set__(self, obj, value):
        return self.setter_method(obj, value)


if __name__ == '__main__':
    class TestClass(object):
        def __init__(self, x, y):
            self._x = x
            self._y = y

        @prop
        def y(self):
            return self._y

        @prop
        def z(self):
            return self._x + self._y

        @prop
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

    t = TestClass(10, 20)
    assert t.z == 30
    assert t.x == 10
    assert t._x == 10
    assert t.y == 20
    assert t._y == 20

    t.x = 567
    assert t.x == 567
    assert t._x == 567
    assert t.z == 567 + 20
