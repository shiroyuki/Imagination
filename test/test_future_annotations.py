from __future__ import annotations

import unittest
from typing import Optional

from imagination import container as c, service
from imagination.decorator.config import (Parameter as PrimitiveParameter,
                                          Service as ServiceParameter,)
from imagination.exc import UnexpectedDefinitionTypeException


class FutureAnnotationsTest(unittest.TestCase):
    """ Regression tests for PEP 563 (`from __future__ import annotations`).

    When annotations are evaluated lazily as strings, the framework must still
    resolve them to concrete types so that auto-wiring and type assertions
    behave exactly as they do with eagerly-evaluated annotations.
    """

    def test_auto_wired_string_annotation(self):
        obj = c.get(StringAutoWiredService)

        self.assertIsInstance(obj, StringAutoWiredService)
        self.assertIsInstance(obj.adapter, StringAutoWiredAdapter)
        self.assertEqual('pong', obj.adapter.ping())

    def test_optional_string_annotation_is_delegated(self):
        obj = c.get(StringOptionalService)

        # An optional (default-valued) dependency is delegated, not auto-wired.
        self.assertIsNone(obj.adapter)

    def test_explicit_service_parameter_with_string_annotation(self):
        obj = c.get(StringExplicitService)

        self.assertIsInstance(obj, StringExplicitService)
        self.assertIsInstance(obj.adapter, StringAutoWiredAdapter)
        self.assertEqual('fooooooo', obj.foo())

    def test_type_assertion_fires_for_wrong_type(self):
        # The declared type annotation is `StringAutoWiredAdapter` but the
        # injected instance is a `StringOtherAdapter`, which is not a subclass.
        with self.assertRaises(UnexpectedDefinitionTypeException):
            c.get(StringMismatchService)

    def test_required_optional_annotation_is_auto_wired(self):
        obj = c.get(StringRequiredOptionalService)

        # `Optional[X]` on a required (no-default) parameter is unwrapped to `X`
        # and auto-wired, exercising the `__unwrap_optional` path.
        self.assertIsInstance(obj, StringRequiredOptionalService)
        self.assertIsInstance(obj.adapter, StringAutoWiredAdapter)
        self.assertEqual('pong', obj.adapter.ping())


@service.registered()
class StringAutoWiredAdapter:
    def ping(self) -> str:
        return 'pong'


@service.registered()
class StringRequiredOptionalService:
    def __init__(self, adapter: Optional[StringAutoWiredAdapter]):
        self.adapter = adapter


@service.registered()
class StringOptionalService:
    def __init__(self, adapter: StringAutoWiredAdapter = None):
        self.adapter = adapter


@service.registered()
class StringAutoWiredService:
    def __init__(self, adapter: StringAutoWiredAdapter):
        self.adapter = adapter


@service.registered(
    params=[
        PrimitiveParameter('Panda', 'name'),
        ServiceParameter(StringAutoWiredAdapter, 'adapter'),
    ],
)
class StringExplicitService:
    def __init__(self, name, adapter: StringAutoWiredAdapter):
        self.name = name
        self.adapter = adapter

    def foo(self) -> str:
        return 'fooooooo'


@service.registered()
class StringOtherAdapter:
    pass


@service.registered(params=[ServiceParameter(StringOtherAdapter, 'dep')])
class StringMismatchService:
    def __init__(self, dep: StringAutoWiredAdapter):
        self.dep = dep
