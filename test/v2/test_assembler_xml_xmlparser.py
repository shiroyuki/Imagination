import sys
import unittest

if sys.version_info >= (3, 3):
    from imagination.debug         import dump_meta_container
    from imagination.assembler.xml import XMLParser


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

    def test_simple(self):
        test_filepath = 'test/data/locator.xml'

        parser = XMLParser()

        self.assertTrue(parser.can_handle(test_filepath))

        containers = parser.parse(test_filepath)

        self.assertEqual(6, len(containers))
