from unittest           import TestCase
from imagination.loader import Loader

# Reference for testing
import dummy.core

class TestLoader(TestCase):
    ''' Test the package loader. '''

    def test_no_loading_on_initialization(self):
        ''' The loader on initialization does nothing. '''

        loader = Loader('dummy.core.PlainOldObject')

        # Make sure that the module and package are not initialized.
        self.assertIsNone(loader._module)
        self.assertIsNone(loader._package)

    def test_path_analysis_on_initialization(self):
        ''' The loader on initialization analyze the package path. '''

        loader = Loader('dummy.core.PlainOldObject')

        # Make sure that all information is ready.
        self.assertEquals(loader._path, 'dummy.core.PlainOldObject')
        self.assertEquals(loader._module_path, 'dummy.core')
        self.assertEquals(loader._package_name, 'PlainOldObject')

    def test_module(self):
        ''' The loader loads the module only when it needs. '''

        loader = Loader('dummy.core.PlainOldObject')

        self.assertIsNone(loader._module)
        self.assertEquals(loader.module, dummy.core)

    def test_package(self):
        ''' The loader loads the package only when it needs. '''

        loader = Loader('dummy.core.PlainOldObject')

        self.assertIsNone(loader._package)
        self.assertEquals(loader.package, dummy.core.PlainOldObject)
