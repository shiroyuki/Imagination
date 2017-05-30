# v2
import contextlib

from ..meta.definition import DataDefinition, ParameterCollection, MethodCall


class DefinitionContext(object):
    def __init__(self, core, metadata):
        self.__core     = core
        self.__metadata = metadata

    @property
    def id(self):
        return self.__metadata.id

    def set_param(self, kind, value, name = None, transformation_required = False):
        """ Define a constructor parameter for a particular entity. """
        self.__metadata.params.add(
            DataDefinition(value, name, kind, transformation_required),
            name,
        )

    def add_dependency(self, dependency_id, name = None):
        """ Inject an entity as a dependency to the specified entity. """
        self.set_param('entity', dependency_id, name, True)

    def add_classinfo(self, fqcn, name = None):
        """ Inject a class/type as a dependency to the specified entity. """
        self.set_param('class', fqcn, name, True)

    @contextlib.contextmanager
    def call(self, method_name : str, origin : str = None):
        """ Declare an initial method call.

            :param str method_name: the name of the executing method.
            :param str origin:      the ID of the alternative target entity.
        """
        target_entity_id  = origin or self.id
        context_reference = MethodCallContext()

        yield context_reference

        method_call = MethodCall(target_entity_id, method_name, context_reference.params)

        self.__core.set_initial_call(method_call)


class MethodCallContext(object):
    def __init__(self):
        self.params = ParameterCollection()

    def with_param(self, kind, value, name = None, transformation_required = False):
        """ Define a constructor parameter for a particular entity. """
        self.params.add(
            DataDefinition(value, name, kind, transformation_required),
            name,
        )

    def with_entity(self, dependency_id, name = None):
        """ Inject an entity as a dependency to the specified entity. """
        self.with_param('entity', dependency_id, name, True)

    def with_type(self, fqcn, name = None):
        """ Inject a class/type as a dependency to the specified entity. """
        self.with_param('class', fqcn, name, True)
