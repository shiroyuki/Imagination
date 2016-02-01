import re
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

    def test_import_non_existing_module(self):
        """ The loader attempts to load a non-existing module. """
        loader = Loader('elephant.wonder')

        self.assertIsNone(loader._package)

        try:
            loader.package()
        except ImportError as e:
            self.assertTrue(self._has_error_message(e, '^No module named'))


    def test_import_non_existing_reference(self):
        """ The loader attempts to load a non-existing reference of an existing module. """
        loader = Loader('imagination.loader.GodLoader')

        self.assertIsNone(loader._package)

        try:
            loader.package()
        except ImportError as e:
            self.assertTrue(self._has_error_message(e, '^Module \'imagination.loader\' has no ref.+ to \'GodLoader\'.+'))

    def _has_error_message(self, exception, pattern):
        return bool(re.search(pattern, exception.msg if hasattr(exception, 'msg') else exception.message))
