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
            'test/data/container-callable.xml',
        ]

        self.assembler = Assembler()
        self.assembler.load(*test_filepaths)

        self.core = self.assembler.core
