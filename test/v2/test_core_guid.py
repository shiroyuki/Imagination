from unittest import TestCase

from imagination.core import Imagination


class UnitTest(TestCase):
    def test_same_core(self):
        a = Imagination()
        b = a

        self.assertEqual(a, b)

    def test_different_core(self):
        a = Imagination()
        b = Imagination()

        self.assertNotEqual(a, b)
