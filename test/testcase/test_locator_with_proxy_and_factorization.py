from os.path  import abspath, dirname, join
from unittest import TestCase

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from imagination.locator          import Locator

# For reference.
from dummy.factorization import Something, Ticker, Manager, Worker

class test_locator_with_proxy_and_factorization(TestCase):
    '''
    Test the locator via the assembler for factorization.
    '''

    def setUp(self):
        self.locator     = Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

    def tearDown(self):
        del self.locator
        del self.transformer
        del self.assembler

    def test_good_locator_xml_on_entity_registration(self):
        self.__prepare_good_locator_from_xml()

        # Normal entity
        self.assertTrue(self.locator.has('manager'), self.locator._entities)

        # Factorized entities
        self.assertTrue(self.locator.has('worker.alpha'))
        self.assertTrue(self.locator.has('worker.bravo'))
        self.assertTrue(self.locator.has('def.doubler'))
        self.assertTrue(self.locator.has('def.trippler'))

    def test_get_object(self):
        self.__prepare_good_locator_from_xml()

        ticker  = self.locator.get('ticker')
        trigger = self.locator.get('something')
        entity  = self.locator.get('worker.alpha')

        self.assertIsInstance(entity, Worker)
        self.assertEqual(entity.name, 'Alpha')
        self.assertEqual(0, len(ticker.sequence))

        trigger.alpha()

        self.assertEqual(1, len(ticker.sequence))

    def test_get_callback(self):
        self.__prepare_good_locator_from_xml()

        ticker  = self.locator.get('ticker')
        trigger = self.locator.get('something')
        doubler = self.locator.get('def.doubler')

        self.assertTrue(callable(doubler))
        self.assertEqual(12, doubler(6))
        self.assertEqual(0, len(ticker.sequence))

        trigger.doubler()

        # No interception for callable object as of 1.9.
        self.assertEqual(0, len(ticker.sequence))

    def __get_data_path(self, filename):
        return abspath(join(dirname(__file__), '..', 'data', filename))

    def __load_from_xml(self, path_from_data):
        test_file = self.__get_data_path(path_from_data)

        self.assembler.load(test_file)

    def __prepare_good_locator_from_xml(self):
        self.__load_from_xml('locator-factorization.xml')