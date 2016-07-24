import sys
import unittest

if sys.version_info >= (3, 3):
    from imagination.debug          import dump_meta_container
    from imagination.assembler.core import Assembler


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

    def test_simple(self):
        test_filepath = 'test/data/locator.xml'

        assembler       = Assembler()
        meta_containers = assembler._load_config_files(test_filepath)

        self.assertIn('poow-1', meta_containers['dioe'].dependencies)
        self.assertIn('poo',    meta_containers['owlad'].dependencies)
