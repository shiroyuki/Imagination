from pprint import pformat
from unittest import TestCase
from imagination import container as c
from imagination.standalone import scan_recursively
from imagination.debug import get_logger

logger = get_logger(__name__)


class UnitTest(TestCase):
    def setUp(self):
        # NOTE: Cannot reset as it is only scan once.
        # c.reset()
        pass

    def test_simple(self):
        self.skipTest('WIP')
        scan_recursively('dummy.dv3')
        logger.debug('All IDs: %s', c.all_ids())
        logger.debug('Extras: %s', pformat([c.get_info(sid).instantiator for sid in c.all_ids()], width=160, indent=4))

    def tearDown(self):
        # NOTE: Cannot reset as it is only scan once.
        # c.reset()
        pass
