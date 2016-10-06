# v2
import inspect

from .debug           import get_logger, dump_meta_container
from .exc             import UnexpectedParameterException, UndefinedDefaultValueException
from .loader          import Loader
from .meta.container  import Container, Entity, Factorization, Lambda
from .meta.definition import ParameterCollection
from .wrapper         import Wrapper


class Controller(object):
    def __init__(self,
                 metadata               : Container,
                 core_get               : callable,
                 core_get_interceptions : callable,
                 transformer_cast       : callable
                 ):
        self.__metadata               = metadata
        self.__core_get               = core_get
        self.__core_get_interceptions = core_get_interceptions
        self.__transformer_cast       = transformer_cast
        self.__logger                 = get_logger('controller/{}'.format(metadata.id))
        self.__container_instance     = None  # Cache
        self.__wrapper_instance       = None  # Wrapper Cache
        self.activation_sequence      = None  # Activation Sequence

    @property
    def metadata(self):
        return self.__metadata

    def activated(self):
        return self.__wrapper_instance is not None or self.__container_instance is not None

    def activate(self):
        if self.activated():
            return self.__wrapper_instance or self.__container_instance

        new_instance = self.__instantiate_container()

        if self.__metadata.cacheable:
            self.__container_instance = new_instance

        interceptions = self.__core_get_interceptions(self.__metadata.id)

        if not interceptions:
            return self.__container_instance

        self.__wrapper_instance = Wrapper(
            self.__core_get,
            self.__container_instance,
            interceptions
        )

        return self.__wrapper_instance

    def __instantiate_container(self):
        metadata       = self.__metadata
        params         = self.__cast_to_params(self.__metadata.params)
        container_type = type(metadata)

        factory_service     = None
        factory_method_name = None
        make_method         = None

        if container_type is Lambda:
            return Loader(metadata.fq_callable_name).package

        if container_type is Entity:
            make_method = Loader(metadata.fqcn).package
        elif container_type is Factorization:
            factory_service     = self.__core_get(metadata.factory_id)
            factory_method_name = metadata.factory_method_name
            make_method         = getattr(factory_service, factory_method_name)

        if not make_method:
            raise NotImplementedError('No make method for {}'.format(container_type.__name__))

        using_parameters = {}
        signature        = inspect.signature(make_method)
        expected_params  = [signature.parameters[name] for name in signature.parameters]
        expected_count   = len(expected_params)

        for index in range(len(params['sequence'])):
            if index >= expected_count:
                raise UnexpectedParameterException('#{}'.format(index))

            definition     = params['sequence'][index]
            expected_param = expected_params[index]

            using_parameters[expected_param.name] = definition

        for name, definition in params['items'].items():
            if name not in signature.parameters:
                raise UnexpectedParameterException('Failed to initiate "{}" due to an unexpected parameter "{}"'.format(metadata.id, name))

            expected_param = signature.parameters[name]

            using_parameters[expected_param.name] = definition

        for expected_param in expected_params:
            param_name = expected_param.name

            if param_name in using_parameters:
                continue

            if expected_param.default == inspect._empty:
                if factory_service:
                    raise UndefinedDefaultValueException(
                        '{factory_class_name}.{factory_method_name}{signature} expects the parameter "{parameter_name}"'.format(
                            factory_class_name  = type(factory_service).__name__,
                            factory_method_name = factory_method_name,
                            signature           = signature,
                            parameter_name      = param_name
                        )
                    )

                raise UndefinedDefaultValueException(
                    '{make_method_name}{signature} expects the parameter "{parameter_name}"'.format(
                        make_method_name  = make_method.__name__,
                        signature         = signature,
                        parameter_name    = param_name
                    )
                )

        return make_method(**using_parameters)

    def __get_parameter_default_value(self, parameter):
        # TODO Use parameter.annotation to check for type.
        if parameter.default == inspect._empty:
            raise UndefinedDefaultValueException(parameter.name)

        return parameter.default

    def __cast_to_params(self, params : ParameterCollection):
        return {
            'sequence': [
                self.__transformer_cast(item)
                for item in params.sequence()
            ],
            'items': {
                key: self.__transformer_cast(value)
                for key, value in params.items()
            },
        }
