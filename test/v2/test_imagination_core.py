import sys
import unittest

from dummy.lazy_action import Alpha, Beta

if sys.version_info >= (3, 3):
    from imagination.debug          import dump_meta_container
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

    def test_get(self):
        alpha = self.core.get('alpha')

        self.assertIsNotNone(alpha)
        self.assertIsInstance(alpha, Alpha)
        self.assertIsInstance(alpha.accompany, Beta)

        self.assertTrue(self.core.get_info('alpha').activated())
        self.assertTrue(self.core.get_info('beta').activated())
        self.assertFalse(self.core.get_info('charlie').activated())
        self.assertFalse(self.core.get_info('poow-1').activated())
