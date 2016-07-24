# v2
from ..debug          import PrintableMixin
from ..helper.general import extract_container_ids_from_parameter_collection
from .definition      import ParameterCollection


class Container(PrintableMixin):
    def __init__(self, identifier : str, kind : str, fqcn : str, params : ParameterCollection = None, cacheable : bool = True):
        assert identifier, 'Container ID must be defined'

        self.__id           = identifier.strip()
        self.__kind         = kind
        self.__fqcn         = fqcn
        self.__params       = params or ParameterCollection()
        self.__cacheable    = cacheable
        self.__dependencies = set() # container ID

        self.__dependency_calculated = False

    @property
    def id(self):
        return self.__id

    @property
    def kind(self):
        return self.__kind

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
