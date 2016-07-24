from os.path  import abspath, dirname, join
from unittest import TestCase

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer

from imagination.action    import Action
from imagination.entity    import Entity
from imagination.exception import UnknownEntityError
from imagination.loader    import Loader
from imagination.locator   import Locator

# For reference.
from dummy.lazy_action import *

class TestAction(TestCase):
    ''' Test concentrating on lazy-loading and actions via the assembler. '''
    def setUp(self):
        self.locator = Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

        filename = 'locator-lazy-action.xml'
        filepath = abspath(join(dirname(__file__), '..', 'data', filename))

        self.assembler.load(filepath)

    def tearDown(self):
        del self.locator
        del self.transformer
        del self.assembler

    def test_interceptable_method(self):
        c = self.locator.get('charlie')

        self.assertIsInstance(c.introduce, Action)
        self.assertEqual(c.name, c.introduce())

    def test_normal_execution(self):
        ''' This is a sanity test. '''

        expected_log_sequence = [
            # sequence as charlie cooks
            'Charlie: introduce itself as "Charlie"',
            'Alpha: order "egg and becon"',
            'Charlie: repeat "egg and becon"',
            'Alpha: confirm for egg and becon',
            'Charlie: respond "wilco"',
            'Charlie: cook',

            # sequence as charlie serves
            'Alpha: speak to Beta, "watch your hand"',
            'Beta: acknowledge',
            'Alpha: wash hands',
            'Charlie: serve'
        ]

        alpha   = self.locator.get('alpha')
        charlie = self.locator.get('charlie')

        charlie.cook()
        charlie.serve()

        self.assertEqual(
            len(expected_log_sequence),
            len(Conversation.logs),
            'The number of sequences in the mock scenario must be the same.'
        )

        for step in range(len(Conversation.logs)):
            expectation = expected_log_sequence[step]
            actual      = Conversation.logs[step]
            self.assertEqual(
                expectation,
                actual,
                'Failed at step {step}: should be "{expectation}", not "{actual}"'.format(
                    step=step,
                    expectation=expectation,
                    actual=actual
                )
            )

        #print '\n'.join(Conversation.logs)