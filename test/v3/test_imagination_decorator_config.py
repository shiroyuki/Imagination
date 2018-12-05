from unittest import TestCase
from imagination import service
from imagination.standalone import container as c
from imagination.decorator.config import (Parameter as PrimitiveParameter,
                                          Service as ServiceParameter,
                                          default_id_naming_strategy)


class UnitTest(TestCase):
    def test_simple(self):
        obj = c.get(SimpleSampleService)

        self.assertIsInstance(obj, SimpleSampleService)
        self.assertEqual('fooooooo', obj.foo())

    def test_parameterized(self):
        obj = c.get(ParameterizedSampleService)

        self.assertIsInstance(obj, ParameterizedSampleService)
        self.assertEqual('fooooooo', obj.foo())


@service(auto_wired=False)
class SimpleSampleService:
    def foo(self) -> str:
        return 'fooooooo'


@service(
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


@service(auto_wired=True)
class AutoWiredService(object):
    pass
