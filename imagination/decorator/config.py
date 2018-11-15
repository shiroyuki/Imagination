# v3
from abc import ABC, abstractproperty
from os import environ
from typing import List, Any, Callable
from imagination.standalone import container as c

def service(id:str = None, params:List[Any] = None, is_primary:bool = False,
            default_service_id_generator:Callable = None):
    """
    Define the class as a service.

    :param str id: Service ID. By default, it will turn the FQCN (module + class name) into the default service ID.
    :param list params: Parameters for the class constructor.
    :param bool is_primary: Flag to determine whether or not this is the primary service of this type
    :param Callable default_service_id_generator: The default service ID generator (factory method)
    """
    cls_props = {}

    def inner_decorator(cls):
        cls_props.update({
            prop_name: getattr(cls, prop_name)
            for prop_name in dir(cls)
            if prop_name == ('__module__', '__name__', '__qualname__', '__dir__', '__doc__')
        })

        generate_default_id = default_service_id_generator or default_id_by_shorten_fully_qualify_class_name

        service_id = id or generate_default_id(cls)  # Figure out the service ID

        with c.define_entity(service_id, default_id_by_fully_qualify_class_name(cls)) as definition:
            for param in (params or []):
                if isinstance(param, Parameter):
                    definition.set_param(param.kind, param.value, param.name)
                elif isinstance(param, Service):
                    definition.add_dependency(param.value, param.name)
                elif isinstance(param, ClassInfo):
                    definition.add_classinfo(param.value, param.name)

        return cls

    for n, v in cls_props.items():
        setattr(inner_decorator, n, v)

    return inner_decorator

def default_id_by_fully_qualify_class_name(cls) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"

def default_id_by_shorten_fully_qualify_class_name(cls) -> str:
    fqcn = default_id_by_fully_qualify_class_name(cls)
    fqcn_segments = fqcn.split('.')
    return f"{'.'.join(s[0].lower() for s in fqcn_segments[:-1])}.{fqcn_segments[-1]}"

def default_id_by_qualify_class_name(cls) -> str:
    return cls.__qualname__

def default_id_by_class_name(cls) -> str:
    return cls.__name__


class AbstractParameter(ABC):
    @abstractproperty
    def name(self):
        raise NotImplementedError()

    @abstractproperty
    def value(self):
        raise NotImplementedError()


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
    def __init__(self, env:str, parse_value:Callable = None, default = None, name=None):
        self._env = env
        self._parse_value = parse_value
        self._default = default
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return type(self.value).__name__

    @property
    def value(self):
        value = environ[self._name]

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
    def __init__(self, service_cls_or_id, name=None, default_service_id_generator:Callable = None):
        self._service_cls_or_id = service_cls_or_id
        self._default_service_id_generator = default_service_id_generator
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        if not isinstance(self._service_cls_or_id, str):
            generate_default_id = self._default_service_id_generator or default_id_by_shorten_fully_qualify_class_name

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