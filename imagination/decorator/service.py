from typing import List, Any, Callable, Optional

from imagination.standalone import container as c
from imagination.helper.general import get_fully_qualified_class_name
from imagination.helper.id_naming import fully_qualified_class_name as default_id_naming_strategy
from .helper import set_parameter


def registered(params: Optional[List[Any]] = None, id: Optional[str] = None, is_primary: Optional[bool] = False,
               auto_wired: Optional[bool] = True, wiring_optional: Optional[bool] = False,
               id_naming_strategy: Optional[Callable] = None):
    """
    Define the class as a service.

    :param list params: Parameters for the class constructor.
    :param str id: Service ID. By default, it will turn the FQCN (module + class name) into the default service ID.
    :param bool is_primary: Flag to determine whether or not this is the primary service of this type
    :param bool auto_wired: Flag to tell Imagination to automatically wire all required dependencies without explicitly
                            specifying them in :param:`params`.
    :param bool wiring_optional: Flag to tell Imagination to also automatically wire optional dependencies if not
                                 explicitly specified. This flag is only used if :param:`auto_wired` is ``True``.
    :param Callable id_naming_strategy: The default service ID generator (factory method)
    """
    cls_props = {}

    def inner_decorator(cls):
        cls_props.update({
            prop_name: getattr(cls, prop_name)
            for prop_name in dir(cls)
            if prop_name == ('__module__', '__name__', '__qualname__', '__dir__', '__doc__')
        })

        service_id = id or (id_naming_strategy or default_id_naming_strategy)(cls)  # Figure out the service ID

        if c.contain(service_id):
            with c.update_definition(service_id) as definition:
                __define_defintion(definition, params)
        else:
            with c.define_entity(service_id, get_fully_qualified_class_name(cls)) as definition:
                __define_defintion(definition, params)

        return cls

    for n, v in cls_props.items():
        setattr(inner_decorator, n, v)

    return inner_decorator


Service = registered
""" Service

.. versionadded:: 3.3
"""


def __define_defintion(definition, params):
    for param in (params or []):
        set_parameter(definition, param)
