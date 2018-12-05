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
            'test/data/locator.xml',
            'test/data/locator-factorization.xml',
            'test/data/locator-lazy-action.xml',
        ]

        self.assembler = Assembler()

    def test_simple(self):
        meta_containers = self.assembler._load_config_files(*self.test_filepaths)

        self.assertIn('poow-1', meta_containers['dioe'].dependencies, meta_containers['dioe'].dependencies)
        self.assertIn('poo',    meta_containers['owlad'].dependencies, meta_containers['owlad'].dependencies)

    def test_activation_order(self):
        pass