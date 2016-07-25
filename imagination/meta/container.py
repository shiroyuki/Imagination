# v2
from ..debug          import PrintableMixin
from ..helper.general import extract_container_ids_from_parameter_collection
from .definition      import ParameterCollection


class FrozenContainerError(RuntimeError):
    """ Error raised when the external code attampts to modify the container while it is frozen. """

class Container(PrintableMixin):
    def __init__(self, identifier : str, cacheable : bool = True):
        assert identifier, 'Container ID must be defined.'

        self.__is_frozen  = False
        self.__cacheable  = cacheable
        self.__identifier = identifier.strip()

    @property
    def id(self):
        return self.__identifier

    @id.setter
    def id(self, new_id : str):
        if self.__is_frozen:
            raise FrozenContainerError('Forbidden to change the identifier in the frozen state')

        self.__identifier = new_id

    @property
    def cacheable(self):
        return self.__cacheable

class Entity(Container):
    def __init__(self, identifier : str, fqcn : str, params : ParameterCollection = None, cacheable : bool = True):
        Container.__init__(self, identifier, cacheable)

        assert fqcn, 'Container\'s class must be defined.'

        self.__fqcn         = fqcn
        self.__params       = params or ParameterCollection()
        self.__dependencies = set() # container ID

        self.__dependency_calculated = False

    @property
    def fqcn(self):
        return self.__fqcn

    @property
    def params(self):
        return self.__params

    @property
    def dependencies(self):
        if not self.__dependency_calculated:
            self.__dependencies.update(
                extract_container_ids_from_parameter_collection(self.__params)
            )

            self.__dependency_calculated = True

        return self.__dependencies

class Factorization(Container):
    def __init__(self, identifier : str, factory_id : str, factory_method_name : str, params : ParameterCollection = None, cacheable : bool = True):
        Container.__init__(self, identifier, cacheable)

        assert factory_id,      'Container\'s factory ID must be defined.'
        assert factory_method_name, 'Container\'s factory method must be defined.'

        self.__factory_id          = factory_id
        self.__factory_method_name = factory_method_name
        self.__params              = params or ParameterCollection()
        self.__dependencies        = set() # container ID

        self.__dependency_calculated = False

    @property
    def factory_id(self):
        return self.__factory_id

    @property
    def factory_method_name(self):
        return self.__factory_method_name

    @property
    def params(self):
        return self.__params

    @property
    def dependencies(self):
        if not self.__dependency_calculated:
            # Add the factory container ID as the primary dependency.
            self.__dependencies.add(self.__factory_id)

            self.__dependencies.update(
                extract_container_ids_from_parameter_collection(self.__params)
            )

            self.__dependency_calculated = True

        return self.__dependencies
