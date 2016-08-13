import sys
import unittest

from dummy.lazy_action import Alpha, Beta

if sys.version_info >= (3, 3):
    from imagination.assembler.core import Assembler
    from imagination.debug          import dump_meta_container
    from imagination.exc            import UndefinedDefaultValueException


class FunctionalTest(unittest.TestCase):
    """ This test is done via the assembler core. """
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

    def test_sample(self):
        test_filepaths = [
            'test/data/locator-instantiation-error.xml',
        ]

        assembler = Assembler()
        assembler.load(*test_filepaths)

        self.assertRaises(UndefinedDefaultValueException, assembler.core.get, 'poow-1')
