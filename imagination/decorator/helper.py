from .config import Parameter, Service, ClassInfo


def set_parameter(definition, param):
    if isinstance(param, Parameter):
        definition.set_param(param.kind, param.value, param.name)
    elif isinstance(param, Service):
        definition.add_dependency(param.value, param.name)
    elif isinstance(param, ClassInfo):
        definition.add_classinfo(param.value, param.name)
