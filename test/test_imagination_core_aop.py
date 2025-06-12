import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# noinspection PyUnresolvedReferences
from dummy.lazy_action import Conversation

from imagination.assembler.core import Assembler


class FunctionalTest(unittest.TestCase):
    """ This test is done via the assembler core. """
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

        test_filepaths = [
            'test/data/locator-aop.xml',
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

    def test_aop_positive(self):
        alpha = self.core.get('alpha')

        # expected_log_sequence = [
        #     # sequence as charlie cooks
        #     'Charlie: introduce itself as "Charlie"',
        #     'Alpha: order "egg and becon"',
        #     'Charlie: repeat "egg and becon"',
        #     'Alpha: confirm for egg and becon',
        #     'Charlie: respond "wilco"',
        #     'Charlie: cook',
        #
        #     # sequence as charlie serves
        #     'Alpha: speak to Beta, "watch your hand"',
        #     'Beta: acknowledge',
        #     'Alpha: wash hands',
        #     'Charlie: serve'
        # ]

        expected_log_sequence = [
            'Alpha: orders "egg"',
            'Beta: acknowledge "egg"',
            'Charlie: cook',
            'Charlie: serve',
            'Beta: says "Merci" to Charlie',
            'Alpha: says "Thank you" to Charlie',
        ]

        conversation = self.core.get('conversation')

        alpha   = self.core.get('alpha')
        charlie = self.core.get('charlie')

        charlie.cook()
        charlie.serve()

        self.assertEqual(
            len(expected_log_sequence),
            len(conversation.logs),
            'The number of sequences in the mock scenario must be the same.'
        )

        self.assertEqual(expected_log_sequence[:4], conversation.logs[:4])

        # NOTE As the order of the last two cannot be guaranteed, the test will
        #      not look into it.
