from os.path  import abspath, dirname, join
from sys      import version_info
from unittest import TestCase

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer

from imagination.entity    import Entity
from imagination.exception import InstantiationError
from imagination.loader    import Loader
from imagination.locator   import Locator
from imagination.action    import Action

class TestLocator(TestCase):
    """ Test the locator via the assembler with instantiation error. """

    def setUp(self):
        self.locator     = Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

    def tearDown(self):
        del self.locator
        del self.transformer
        del self.assembler

    def test_error_detection(self):
        actual_exception = None

        try:
            self.__load_from_xml('locator-instantiation-error.xml')
        except InstantiationError as e:
            actual_exception = e # Expected error

        # just to verify
        self.assertIsInstance(actual_exception, InstantiationError)
        self.assertRegex(
            str(actual_exception),
            'entity "poow-1".+a, b, do_.+provide.+do_.+bool\)' \
                if version_info > (3,3) \
                else 'entity "poow-1".+\(\.\.\.\)'
        ) # Python 2.7 will have less feedback.

    def __get_data_path(self, filename):
        return abspath(join(dirname(__file__), '..', 'data', filename))

    def __load_from_xml(self, path_from_data):
        test_file = self.__get_data_path(path_from_data)

        self.assembler.load(test_file)

    def __prepare_good_locator_from_xml(self):
        self.__load_from_xml('locator.xml')
