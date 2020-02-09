# v3
from abc import ABC, abstractmethod
from os import environ, getenv
from typing import Callable, Optional, Any
from imagination.helper.id_naming import fully_qualified_class_name as default_id_naming_strategy


class AbstractParameter(ABC):
    @property
    @abstractmethod
    def name(self):
        ...

    @property
    @abstractmethod
    def value(self):
        ...


class Parameter(AbstractParameter):
    """ Primitive-type Parameter """

    def __init__(self, value, name=None):
        self._value = value
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return type(self.value).__name__

    @property
    def value(self):
        return self._value


class EnvironmentVariable(AbstractParameter):
    def __init__(self, env: str, parse_value: Callable = None, default: Any = None,
                 allow_default: Optional[bool] = None, name: str = None):
        self._env = env
        self._parse_value = parse_value
        self._default = default
        self._allow_default = allow_default or False
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return type(self.value).__name__

    @property
    def value(self):
        value = getenv(self._env) if self._allow_default else environ[self._env]

        if self._parse_value is not None:
            value = self._parse_value(value)

        if value is None:
            return self._default

        return value


class Service(AbstractParameter):
    """
    Service Parameter

    :param service_cls_or_id: Service class (type) or ID (string). When a class (type) is provided, it will try to
                              figure out by the default ID or ``primary``.
    """

    def __init__(self, service_cls_or_id, name=None, id_naming_strategy: Callable = None):
        self._service_cls_or_id = service_cls_or_id
        self._id_naming_strategy = id_naming_strategy
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        if not isinstance(self._service_cls_or_id, str):
            generate_default_id = self._id_naming_strategy or default_id_naming_strategy

            return generate_default_id(self._service_cls_or_id)

        return self._service_cls_or_id


class ClassInfo(AbstractParameter):
    """
    Class/Type Parameter

    :param fqcn: Fully qualified class name
    """

    def __init__(self, fqcn, name=None):
        self._fqcn = fqcn
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._fqcn
