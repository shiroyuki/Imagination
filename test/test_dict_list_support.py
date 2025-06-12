import sys
import unittest

if sys.version_info >= (3, 3):
    from imagination.debug          import dump_meta_container
    from imagination.assembler.core import Assembler


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

        self.test_filepaths = [
            'test/data/locator-strategy.xml',
        ]

        self.assembler = Assembler()

    def test_simple(self):
        self.assembler.load(*self.test_filepaths)

        container = self.assembler.core

        ctrl = container.get('strategy.controller')

        self.assertEqual(2, len(ctrl.strategy_mapping))
        self.assertEqual(2, len(ctrl.strategy_order))
