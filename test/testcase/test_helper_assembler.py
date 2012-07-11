from os.path               import abspath, dirname, join
from unittest              import TestCase

from imagination.entity    import Entity
from imagination.exception import *
from imagination.loader    import Loader
from imagination.locator   import Locator

from imagination.helper.assembler import Assembler
from imagination.helper.meta      import Transformer

class TestHelperAssembler(TestCase):
    def setUp(self):
        self.locator     = Locator()
        self.transformer = Transformer(self.locator)

        self.filename = 'locator-lazy-action.xml'
        self.filepath = abspath(join(dirname(__file__), '..', 'data', self.filename))

        #self.locator.load_xml(filepath)

    def tearDown(self):
        del self.locator
        del self.transformer

    def test_initialization(self):
        assembler = Assembler(self.transformer)

    def test_only_loading(self):
        assembler = Assembler(self.transformer)
        assembler.load(self.filepath)