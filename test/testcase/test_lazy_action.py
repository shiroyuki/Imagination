from os.path  import abspath, dirname, join
from unittest import TestCase

from imagination.helper.assembler import Assembler
from imagination.helper.meta      import Transformer

from imagination.entity    import Entity
from imagination.exception import UnknownEntityError
from imagination.loader    import Loader
from imagination.locator   import Locator

# For reference.
from dummy.lazy_action import *

class TestLazyAction(TestCase):
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

    def test_lazy_initialization(self):
        self.assertIsInstance(self.locator.get('alpha').call_accompany(), Beta)
        self.assertIsInstance(self.locator.get('beta'), Beta)

        self.assertEquals(self.locator.get('alpha').call_accompany(), self.locator.get('beta'))

    def test_actions(self):
        self.locator.get('charlie').cook()

        #print
        #print '\n'.join(Conversation.logs)
        #print