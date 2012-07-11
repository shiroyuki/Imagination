from unittest import TestCase

from imagination.decorator.validator import *
from imagination.exception import MisplacedValidatorError

class TestLazyAction(TestCase):
    def test_method_permitive_good(self):
        foo(2)
        foo(-2)
        foo(01)

    def test_method_permitive_bad(self):
        try:
            foo(2.0)
        except TypeError, e:
            self.assertEqual('int', e.message)

    def test_method_instance(self):
        f = Foo()

        bar(f)

    def test_class_method(self):
        f = Foo()
        f.b(1)

    def test_class_constructor_exception(self):
        try:
            @allowed_type(int)
            class Bar(object):
                def __init__(self, b):
                    b = b
            
            this.assertTrue(False)
        except MisplacedValidatorError, e:
            pass

class Foo(object):
    a = 1

    @allowed_type(int)
    def b(self, b):
        return b

@allowed_type(int)
def foo(a):
    return a

@allowed_type(Foo)
def bar(b):
    return b

@allowed_type(None, unicode, type)
def goo(*args):
    pass
