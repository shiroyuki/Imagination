from os.path               import abspath, dirname, join
from unittest              import TestCase

from imagination.entity    import Entity
from imagination.exception import *
from imagination.loader    import Loader
from imagination.locator   import Locator

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer

class TestHelperAssembler(TestCase):
    def setUp(self):
        self.locator     = Locator()
        self.transformer = Transformer(self.locator)

        self.filename = 'locator-lazy-action.xml'
        self.filepath = self.__filepath(self.filename)

    def __filepath(self, where):
        return abspath(join(dirname(__file__), '..', 'data', where))

    def tearDown(self):
        del self.locator
        del self.transformer

    def test_initialization_good(self):
        assembler = Assembler(self.transformer)

    def test_initialization_failed_on_multiple_events(self):
        assembler = Assembler(self.transformer)

        try:
            assembler.load(self.__filepath('locator-lazy-action-malform.xml'))
            self.assertTrue(False, 'Passed where it should have failed.')
        except MultipleInterceptingEventsWarning:
            self.assertTrue(True)

    def test_only_loading(self):
        assembler = Assembler(self.transformer)
        assembler.load(self.filepath)