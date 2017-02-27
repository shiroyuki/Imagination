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

    def test_no_params(self):
        alpha = self.core.get('alpha')

        try:
            alpha.init_self_destruction_1()
        except DummyException as e:
            self.assertIsInstance(e.previous_error, RuntimeError)
            self.assertFalse(e.positional_parameters)
            self.assertFalse(e.keyword_parameters)
        else:
            self.assertTrue(False, "This is supposed to be raised an exception.")

    def test_with_params(self):
        alpha = self.core.get('alpha')

        positional_parameters = (1, 2, 3)
        keyword_parameters    = {'d': 4, 'e': 5}

        try:
            alpha.init_self_destruction_2(*positional_parameters, **keyword_parameters)
        except DummyException as e:
            self.assertIsInstance(e.previous_error, RuntimeError)
            self.assertEqual(positional_parameters, e.positional_parameters)
            self.assertEqual(keyword_parameters,    e.keyword_parameters)
        else:
            self.assertTrue(False, "This is supposed to be raised an exception.")
