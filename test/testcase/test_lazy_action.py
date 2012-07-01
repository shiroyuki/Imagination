from os.path               import abspath, dirname, join
from unittest              import TestCase
from imagination.entity    import Entity
from imagination.exception import UnknownEntityError
from imagination.loader    import Loader
from imagination.locator   import Locator

# For reference.
from dummy.core            import PlainOldObject
from dummy.core            import PlainOldObjectWithParameters

class TestLazyAction(TestCase):
    def setUp(self):
        self.locator = Locator()

        filename = 'locator-lazy-action.xml'
        filepath = abspath(join(dirname(__file__), '..', 'data', filename))

        self.locator.load_xml(filepath)

    def tearDown(self):
        del self.locator

    def test_initialization(self):
        pass