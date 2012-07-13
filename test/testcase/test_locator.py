from os.path               import abspath, dirname, join
from unittest              import TestCase
from imagination.entity    import Entity
from imagination.exception import UnknownEntityError
from imagination.loader    import Loader
from imagination.locator   import Locator

# For reference.
from dummy.core            import PlainOldObject
from dummy.core            import PlainOldObjectWithParameters

class TestLocator(TestCase):
    class UnknownEntity(object): pass

    def setUp(self):
        self.locator = Locator()

    def tearDown(self):
        del self.locator

    def __make_good_entity(self):
        return Entity(
            'poo', Loader('dummy.core.PlainOldObject')
        )

    def test_checker(self):
        entity = self.__make_good_entity()

        self.assertFalse(self.locator.has('poo'))
        self.assertRaises(UnknownEntityError, self.locator.get, ('poo'))

    def test_before_activation(self):
        entity = self.__make_good_entity()

        self.locator.set('poo', entity)

        self.assertTrue(self.locator.has('poo'))
        self.assertFalse(entity.activated())

    def test_after_activation(self):
        entity = self.__make_good_entity()

        self.locator.set('poo', entity)

        self.assertIsInstance(self.locator.get('poo'), PlainOldObject)
        self.assertTrue(entity.activated())

    def __get_data_path(self, filename):
        return abspath(join(dirname(__file__), '..', 'data', filename))

    def __prepare_good_locator_from_xml(self):
        test_file = self.__get_data_path('locator.xml')

        self.locator.load_xml(test_file)

    def test_good_locator_xml_on_entity_registration(self):
        self.__prepare_good_locator_from_xml()

        self.assertTrue(self.locator.has('poo'))
        self.assertTrue(self.locator.has('poow-1'))
        self.assertTrue(self.locator.has('poow-2'))
        self.assertTrue(self.locator.has('dioc'))
        self.assertTrue(self.locator.has('dioe'))

    def test_good_locator_xml_on_class_injection(self):
        self.__prepare_good_locator_from_xml()

        self.assertEqual(self.locator.get('dioc').r, PlainOldObject)

    def test_good_locator_xml_on_class_injection(self):
        self.__prepare_good_locator_from_xml()

        self.assertIsInstance(self.locator.get('dioe').e, PlainOldObjectWithParameters)

    def test_entities_with_same_class(self):
        self.__prepare_good_locator_from_xml()

        self.assertIsInstance(self.locator.get('poow-1'), PlainOldObjectWithParameters)
        self.assertIsInstance(self.locator.get('poow-2'), PlainOldObjectWithParameters)

        self.assertNotEquals(self.locator.get('poow-1').method(), self.locator.get('poow-2').method())
        self.assertEquals('%.2f' % self.locator.get('poow-1').method(), '0.67')
        self.assertEquals(self.locator.get('poow-2').method(), 35)
