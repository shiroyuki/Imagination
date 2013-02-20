from os.path  import abspath, dirname, join
from unittest import TestCase

from imagination.exception import *
from imagination.locator   import Locator

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from dummy.core import PlainOldObject


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

        self.assertRaises(MultipleInterceptingEventsWarning, assembler.load, self.__filepath('locator-lazy-action-malform.xml'))

    def test_only_loading(self):
        assembler = Assembler(self.transformer)

        assembler.load(self.filepath)

    def test_list_support(self):
        assembler = Assembler(self.transformer)

        assembler.load(self.__filepath('locator.xml'))

        obj = assembler.locator.get('owlad')

        self.assertIsInstance(obj.l, list)
        self.assertIsInstance(obj.l[1], int)
        self.assertIsInstance(obj.l[2], list)
        self.assertIsInstance(obj.l[2][0], PlainOldObject)
        self.assertIsInstance(obj.t, tuple)
        self.assertIsInstance(obj.d, dict)