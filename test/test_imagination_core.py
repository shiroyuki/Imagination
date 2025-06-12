import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# noinspection PyUnresolvedReferences
from dummy.factorization import Manager, Worker
# noinspection PyUnresolvedReferences
from dummy.lazy_action import Alpha, Beta

from imagination.wrapper import Wrapper
from imagination.assembler.core import Assembler


class FunctionalTest(unittest.TestCase):
    """ This test is done via the assembler core. """
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

        test_filepaths = [
            'test/data/locator.xml',
            'test/data/locator-factorization.xml',
            'test/data/locator-lazy-action.xml',
            'test/data/container-callable.xml',
        ]

        self.assembler = Assembler()
        self.assembler.load(*test_filepaths)

        self.core = self.assembler.core

    def test_calculate_activation_sequence(self):
        alpha_metadata      = self.core.get_metadata('alpha')
        activation_sequence = self.core._calculate_activation_sequence('alpha')

        minimum_dependencies = alpha_metadata.dependencies
        common_dependencies  = set(activation_sequence).intersection(minimum_dependencies)

        self.assertEqual(len(minimum_dependencies), len(common_dependencies))

    def test_get_entity(self):
        alpha = self.core.get('alpha')

        self.assertIsNotNone(alpha)
        self.assertIsInstance(alpha, Wrapper)
        self.assertIsInstance(alpha._internal_instance, Alpha)
        self.assertIsInstance(alpha.accompany, Wrapper)
        self.assertIsInstance(alpha.accompany._internal_instance, Beta)

        self.assertTrue(self.core.get_info('alpha').activated())
        self.assertTrue(self.core.get_info('beta').activated())
        self.assertFalse(self.core.get_info('charlie').activated())
        self.assertFalse(self.core.get_info('poow-1').activated())

    def test_get_factorization(self):
        alpha = self.core.get('worker.alpha')

        self.assertIsNotNone(alpha)
        self.assertIsInstance(alpha, Wrapper)
        self.assertIsInstance(alpha._internal_instance, Worker)

        self.assertTrue(self.core.get_info('worker.alpha').activated())
        self.assertTrue(self.core.get_info('manager').activated())
        self.assertFalse(self.core.get_info('worker.bravo').activated())
        self.assertFalse(self.core.get_info('something').activated())

    def test_get_lambda(self):
        func_foo = self.core.get('func_foo')

        self.assertTrue(callable(func_foo))

        self.assertTrue(self.core.get_info('func_foo').activated())
        self.assertFalse(self.core.get_info('alpha').activated())
        self.assertFalse(self.core.get_info('beta').activated())
        self.assertFalse(self.core.get_info('charlie').activated())
        self.assertFalse(self.core.get_info('poow-1').activated())

        # Check if everything is still working.
        self.assertEqual(func_foo(1, 2, 3), 1)
        self.assertEqual(func_foo(1, 2, 3, 4), 2)
