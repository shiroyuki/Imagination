from pprint import pprint
from typing import Optional
from unittest import TestCase
from imagination import container as c, service
from imagination.standalone import scan_recursively

class UnitTest(TestCase):
    def setUp(self):
        c.reset()

    def test_simple(self):
        scan_recursively('dummy.dv3')
        print(c.all_ids())
        pprint([c.get_info(sid).instantiator for sid in c.all_ids()], width=160, indent=4)

    def tearDown(self):
        c.reset()