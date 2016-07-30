# v2
from ..debug          import PrintableMixin
from ..helper.general import extract_container_ids_from_parameter_collection
from .definition      import ParameterCollection


class FrozenContainerError(RuntimeError):
    """ Error raised when the external code attampts to
        modify the container while it is frozen.
    """


class Container(PrintableMixin):
    def __init__(self,
                 identifier   : str,
                 params       : ParameterCollection = None,
                 interception : list = [],
                 cacheable    : bool = True
                 ):
        assert identifier, 'Container ID must be defined.'

        self._is_frozen    = False
        self._cacheable    = cacheable
        self._identifier   = identifier.strip()
        self._params       = params or ParameterCollection()
        self._dependencies = set()  # Container ID

        self._dependency_calculated = False

    @property
    def id(self):
        return self._identifier

    @id.setter
    def id(self, new_id : str):
        if self._is_frozen:
            raise FrozenContainerError(
                'Forbidden to change the identifier in the frozen state'
            )

        self._identifier = new_id

    @property
    def params(self):
        return self._params

    @property
    def cacheable(self):
        return self._cacheable

    @property
    def dependencies(self):
        if not self._dependency_calculated:
            self._dependencies.update(
                extract_container_ids_from_parameter_collection(self._params)
            )

            self._dependency_calculated = True

        return self._dependencies


class Entity(Container):
    def __init__(self,
                 identifier : str,
                 fqcn       : str,
                 params     : ParameterCollection = None,
                 cacheable  : bool = True
                 ):
        Container.__init__(self, identifier, params, cacheable)

        assert fqcn, 'Container\'s class must be defined.'

        self._fqcn = fqcn

    @property
    def fqcn(self):
        return self._fqcn


class Factorization(Container):
    def __init__(self,
                 identifier          : str,
                 factory_id          : str,
                 factory_method_name : str,
                 params              : ParameterCollection = None,
                 cacheable           : bool = True
                 ):
        Container.__init__(self, identifier, params, cacheable)

        assert factory_id,          'Undefined factory ID'
        assert factory_method_name, 'Undefined factory method'

        self._factory_id          = factory_id
        self._factory_method_name = factory_method_name

    @property
    def factory_id(self):
        return self._factory_id

    @property
    def factory_method_name(self):
        return self._factory_method_name

    @property
    def dependencies(self):
        if not self._dependency_calculated:
            # Add the factory container ID as the primary dependency.
            self._dependencies.add(self._factory_id)

            self._dependencies.update(
                extract_container_ids_from_parameter_collection(self._params)
            )

            self._dependency_calculated = True

        return self._dependencies


class LambdaUnusedParameterWarning(RuntimeWarning):
    """ Warning when the parameters are defined but
        the framework does not support at the moment.
    """


class Lambda(Container):
    def __init__(self,
                 identifier       : str,
                 fq_callable_name : str,
                 params           : ParameterCollection = None,
                 cacheable        : bool = True
                 ):
        Container.__init__(self, identifier, params, cacheable)

        assert fq_callable_name, 'Undefined callable'

        self._fq_callable_name = fq_callable_name

        if params and len(params):
            raise LambdaUnusedParameterWarning('The parameters will not be used.')

    @property
    def fq_callable_name(self):
        return self._fq_callable_name
