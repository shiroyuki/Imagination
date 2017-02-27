import sys
import unittest

if sys.version_info >= (3, 3):
    from imagination.debug          import dump_meta_container
    from imagination.assembler.core import Assembler
    from imagination.wrapper        import Wrapper

from dummy.aop_error_event import Alpha, DummyException

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

        # print(dir(alpha))
        # for pn in dir(alpha):
        #     pv = getattr(alpha, pn)
        #
        #     print('{} => {}'.format(pn, pv))
        #     print('-' * 120)
        #     print(pv.__doc__)
        #     print()

        self.assertIsInstance(alpha, Wrapper)
        self.assertIsInstance(alpha, Alpha)

        try:
            alpha.init_self_destruction_1()

            self.assertTrue(False, "This is supposed to be raised an exception.")
        except DummyException as e:
            self.assertIsInstance(e.previous_error, RuntimeError)
