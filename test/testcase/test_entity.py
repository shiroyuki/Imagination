from unittest              import TestCase
from imagination.loader    import Loader
from imagination.entity    import Entity
from imagination.exception import *

# Reference for testing
import dummy.core

class TestEntity(TestCase):
    class UnknownLoader(object): pass

    def setUp(self):
        self.plainLoader = Loader('dummy.core.PlainOldObject')
        self.paramLoader = Loader('dummy.core.PlainOldObjectWithParameters')
        self.falseLoader = self.UnknownLoader()

    def tearDown(self):
        del self.plainLoader
        del self.paramLoader
        del self.falseLoader

    def test_fork(self):
        e = Entity('test-object', self.plainLoader)

        a = e.fork()
        b = e.fork()

        self.assertTrue(a is not None)
        self.assertTrue(b is not None)
        self.assertNotEquals(a, b);
        self.assertFalse(e.activated)

    def test_initialization_with_no_args(self):
        e = Entity('test-object', self.plainLoader)

        self.assertFalse(e.activated)
        self.assertEquals(e.instance.method(), 0)
        self.assertTrue(e.activated)

        a = e.instance
        b = e.instance

        self.assertTrue(a is not None)
        self.assertTrue(b is not None)
        self.assertEquals(a, b);

    def test_with_only_list_args(self):
        e = Entity('test-object', self.paramLoader, 2, 3)

        self.assertFalse(e.activated)
        self.assertEqual(e.instance.a, 2)
        self.assertEquals(e.instance.method(), 6)
        self.assertTrue(e.activated)

    def test_with_only_dict_args(self):
        e = Entity('test-object', self.paramLoader, 5, b=7)

        self.assertFalse(e.activated)
        self.assertEqual(e.instance.b, 7)
        self.assertEquals(e.instance.method(), 35)
        self.assertTrue(e.activated)

    def test_with_mixed_args(self):
        e = Entity('test-object', self.paramLoader, b=11, a=13)

        self.assertFalse(e.activated)
        self.assertEqual(e.instance.a, 13)
        self.assertEquals(e.instance.method(), 143)
        self.assertTrue(e.activated)

    def test_loader_exception(self):
        try:
            e = Entity('test-object', self.falseLoader, 17, 19)
            self.assertTrue(False)
        except TypeError:
            pass
