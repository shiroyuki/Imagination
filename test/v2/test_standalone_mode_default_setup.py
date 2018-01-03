from unittest import TestCase

from imagination.standalone import container


class UnitTest(TestCase):
    def test_default_setup(self):
        """ Test the default setup

            This is to ensure that the container is already ready by the time
            the standalone module is loaded.
        """
        self.assertIsNotNone(container)
        self.assertIsNotNone(container.guid)
