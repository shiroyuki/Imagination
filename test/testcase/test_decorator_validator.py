from unittest import TestCase

from imagination.decorator.validator import *
from imagination.exception import MisplacedValidatorError

class TestLazyAction(TestCase):
    def test_method_permitive_good(self):
        foo(2)
        foo(-2)

    def test_method_permitive_bad(self):
        try:
            foo(2.0)
            self.assertTrue(False)
        except TypeError as e:
            actual_message = str(e.message if 'message' in dir(e) else e)

            self.assertEqual('Argument #0 was excepting int but float has been given.', actual_message)

    def test_method_instance(self):
        f = Foo()

        bar(f)

    def test_class_method(self):
        f = Foo()
        f.b(1)

    def test_class_constructor_exception(self):
        try:
            @restrict_type(int)
            class Bar(object):
                def __init__(self, b):
                    b = b

            self.assertTrue(False)
        except MisplacedValidatorError as e:
            pass

class Foo(object):
    a = 1

    @restrict_type(int)
    def b(self, b):
        return b

@restrict_type(int)
def foo(a):
    return a

@restrict_type(Foo)
def bar(b):
    return b
