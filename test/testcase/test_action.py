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

    def test_actions_without_events(self):
        c = self.locator.get('charlie')

        self.assertIsInstance(c.introduce, Action)
        self.assertEquals(c.name, c.introduce())

    def test_actions(self):
        ''' This is NOT a test. '''
        #alpha   = self.locator.get('alpha')
        charlie = self.locator.get('charlie')

        charlie.cook()

        #alpha.order('news')

        #print '\n'.join(Conversation.logs)