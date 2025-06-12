from unittest import TestCase

from imagination.core import Imagination


class UnitTest(TestCase):
    def test_minimum(self):
        """ Test the proxy mode of the core container.

            This is to ensure that the standalone container (AKA core) is
            properly replaced when we needed.
        """
        sample_entity_id = 'foo'

        # Set up the dummy containers.
        container_a = Imagination()
        container_b = Imagination()

        # Set up a dummy definition in the container B.
        with container_b.define_entity(sample_entity_id, 're.compile') as entity:
            entity.set_param('str', 'abc')

        # Ensure the pre-test conditions.
        self.assertFalse(container_a.in_proxy_mode())
        self.assertFalse(container_a.contain(sample_entity_id))

        self.assertFalse(container_b.in_proxy_mode())
        self.assertTrue(container_b.contain(sample_entity_id))

        # Trigger the proxy mode.
        container_a.act_as(container_b)

        # Assert the post condition.
        self.assertNotEqual(container_a, container_b)

        self.assertTrue(container_a.in_proxy_mode())
        self.assertTrue(container_a.contain(sample_entity_id))

        self.assertFalse(container_b.in_proxy_mode())
        self.assertTrue(container_b.contain(sample_entity_id))
