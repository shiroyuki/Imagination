from os.path               import abspath, dirname, join
from unittest              import TestCase

#from imagination.entity    import Entity
from imagination.exception import *
#from imagination.loader    import Loader
#from imagination.locator   import Locator

from imagination.helper.assembler import Assembler

# For reference.
from dummy.lazy_action import *

class TestHelperAssembler(TestCase):
    def setUp(self):
        '''
        self.locator = Locator()

        filename = 'locator-lazy-action.xml'
        filepath = abspath(join(dirname(__file__), '..', 'data', filename))

        self.locator.load_xml(filepath)
        '''

    def tearDown(self):
        #del self.locator
        pass

    def test_initialization(self):
        #assembler = Assembler(None)
        pass
