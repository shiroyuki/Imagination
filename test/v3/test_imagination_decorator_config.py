from unittest import TestCase
from imagination import service
from imagination.standalone import container as c
from imagination.decorator.config import default_id_by_fully_qualify_class_name, \
                                         default_id_by_shorten_fully_qualify_class_name, \
                                         default_id_by_qualify_class_name, \
                                         default_id_by_class_name, \
                                         Parameter as PrimitiveParameter, \
                                         Service as ServiceParameter


@service(default_service_id_generator=default_id_by_class_name)
class SimpleSampleService:
    def foo(self) -> str:
        return 'fooooooo'


@service(
    params=[
        PrimitiveParameter('Panda', 'name'),
        ServiceParameter(SimpleSampleService, 'simple_sample', default_id_by_class_name),
    ],
    default_service_id_generator=default_id_by_class_name
)
class ParameterizedSampleService:
    def __init__(self, name, simple_sample:SimpleSampleService):
        pass
    def foo(self) -> str:
        return 'fooooooo'


class UnitTest(TestCase):
    def test_default_id_generators(self):
        test_class = SimpleSampleService
        self.assertEqual(
            'test_imagination_decorator_config.SimpleSampleService',
            default_id_by_fully_qualify_class_name(test_class),
        )
        self.assertEqual(
            't.SimpleSampleService',
            default_id_by_shorten_fully_qualify_class_name(test_class),
        )
        # self.assertEqual(
        #     'UnitTest.SimpleSampleService',
        #     default_id_by_qualify_class_name(test_class),
        # )
        self.assertEqual(
            'SimpleSampleService',
            default_id_by_class_name(test_class),
        )

    def test_simple(self):
        obj = c.get('SimpleSampleService')

        self.assertIsInstance(obj, SimpleSampleService)
        self.assertEqual('fooooooo', obj.foo())

    def test_parameterized(self):
        obj = c.get('ParameterizedSampleService')

        self.assertIsInstance(obj, ParameterizedSampleService)
        self.assertEqual('fooooooo', obj.foo())