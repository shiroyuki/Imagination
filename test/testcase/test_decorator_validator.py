from unittest import TestCase

from imagination.decorator.validator import *

class TestLazyAction(TestCase):
    def test_method_permitive_good(self):
        foo(2)
        foo(-2)
        foo(01)

    def test_method_permitive_bad(self):
        try:
            foo(2.0)
        except AssertionError, e:
            self.assertEqual('int', e.message)

    def test_method_instance(self):
        f = Foo()

        bar(f)

    def test_class_method_good(self):
        b = Bar(2)

    def test_class_method_bad(self):
        try:
            b = Bar(2.0)
        except AssertionError, e:
            self.assertEqual('int', e.message)

class Foo(object):
    a = 1

@allowed_type(int)
class Bar(object):
    def __init__(self, b):
        b = b

@allowed_type(int)
def foo(a):
    return a

@allowed_type(Foo)
def bar(b):
    return b

@allowed_type(None, unicode, type)
def goo(*args):
    pass