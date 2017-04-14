import os
import unittest

from imagination.exc                import UnknownEnvironmentVariableError
from imagination.helper.transformer import Transformer


class UnitTest(unittest.TestCase):
    def setUp(self):
        # Not passing anything as the core is not needed for this test
        self.transformer = Transformer(None)

    def test_pre_process_with_valid_env(self):
        expectation = 'Hello, {}. Is your home at {}?'.format(os.getenv('USER'), os.getenv('HOME'))
        input_data  = 'Hello, { $USER }. Is your home at { $HOME }?'

        self.assertEqual(expectation, self.transformer._pre_process(input_data))

    def test_pre_process_with_default_value_as_string(self):
        expectation = 'I like sushi.'
        input_data  = 'I like { $FOOD or "sushi" }.'

        self.assertEqual(expectation, self.transformer._pre_process(input_data))

    def test_pre_process_with_default_value_as_float(self):
        expectation = 'The interest rate is 1.25%.'
        input_data  = 'The interest rate is { $INTEREST_RATE or 1.25 }%.'

        self.assertEqual(expectation, self.transformer._pre_process(input_data))

    def test_pre_process_with_default_value_as_int(self):
        expectation = 'There are 17 eggs in this room.'
        input_data  = 'There are { $HEAD_COUNT or 17 } eggs in this room.'

        self.assertEqual(expectation, self.transformer._pre_process(input_data))

    def test_pre_process_with_unknown_env(self):
        input_data = 'There are { $HEAD_COUNT } eggs in this room.'

        with self.assertRaises(UnknownEnvironmentVariableError):
            self.transformer._pre_process(input_data)
