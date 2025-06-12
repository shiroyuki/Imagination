import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# noinspection PyUnresolvedReferences
from dummy.aop_error_event import Alpha, DummyException

from imagination.assembler.core import Assembler
from imagination.wrapper import Wrapper


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

        test_filepaths = [
            'test/data/locator-aop-error-event.xml',
        ]

        self.assembler = Assembler()
        self.assembler.load(*test_filepaths)

        self.core = self.assembler.core

    def test_simple(self):
        alpha = self.core.get('alpha')

        self.assertIsInstance(alpha, Wrapper)
        self.assertIsInstance(alpha, Alpha)
        self.assertTrue(issubclass(type(alpha), (Wrapper, Alpha)))
