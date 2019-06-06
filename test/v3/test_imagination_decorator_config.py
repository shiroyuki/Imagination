from typing import Optional
from unittest import TestCase
from imagination import container as c, service
from imagination.decorator.config import (Parameter as PrimitiveParameter,
                                          Service as ServiceParameter,)
from imagination.debug import get_logger

logger = get_logger(__name__)


class UnitTest(TestCase):
    def setUp(self):
        # NOTE: Cannot reset as it is only scan once.
        # c.reset()
        pass

    def tearDown(self):
        # NOTE: Cannot reset as it is only scan once.
        # c.reset()
        pass

    def test_simple(self):
        obj = c.get(SimpleSampleService)

        self.assertIsInstance(obj, SimpleSampleService)
        self.assertEqual('fooooooo', obj.foo())

    def test_parameterized(self):
        obj = c.get(ParameterizedSampleService)

        self.assertIsInstance(obj, ParameterizedSampleService)
        self.assertEqual('fooooooo', obj.foo())

    def test_auto_wiring(self):
        _ = c.get(NormalAutoWiredService)


@service.registered(auto_wired=False)
class SimpleSampleService:
    def foo(self) -> str:
        return 'fooooooo'


@service.registered(
    auto_wired=False,
    params=[
        PrimitiveParameter('Panda', 'name'),
        ServiceParameter(SimpleSampleService, 'simple_sample'),
    ],
)
class ParameterizedSampleService:
    def __init__(self, name, simple_sample:SimpleSampleService):
        pass

    def foo(self) -> str:
        return 'fooooooo'


@service.registered(auto_wired=True, params=[PrimitiveParameter(123, 'b'), PrimitiveParameter('something', 'c')])
class NormalAutoWiredService(object):
    def __init__(self, a:ParameterizedSampleService, b:int, c, d:Optional[SimpleSampleService] = None):
        pass

@service.registered(auto_wired=True, wiring_optional=True)
class FullAutoWiredService(object):
    def __init__(self, a:ParameterizedSampleService, b:int, c, d:Optional[SimpleSampleService] = None):
        pass
