from os.path               import abspath, dirname, join
from unittest              import TestCase
from imagination.entity    import Entity
from imagination.exception import UnknownEntityError
from imagination.loader    import Loader
from imagination.locator   import Locator

# For reference.
from dummy.lazy_action import *

class TestLazyAction(TestCase):
    def setUp(self):
        self.locator = Locator()

        filename = 'locator-lazy-action.xml'
        filepath = abspath(join(dirname(__file__), '..', 'data', filename))

        self.locator.load_xml(filepath)

    def tearDown(self):
        del self.locator

    def test_lazy_initialization(self):
        self.assertIsInstance(self.locator.get('alpha').call_accompany(), Beta)
        self.assertIsInstance(self.locator.get('beta'), Beta)

        self.assertEquals(self.locator.get('alpha').call_accompany(), self.locator.get('beta'))

    def test_actions(self):
        self.locator.get('charlie').cook()

        #print
        #print '\n'.join(Conversation.logs)
        #print