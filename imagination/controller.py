# v2
import inspect

from .debug           import get_logger, dump_meta_container
from .exc             import UnexpectedParameterException, UndefinedDefaultValueException, \
                             UnexpectedDefinitionTypeException, MissingParameterException
from .loader          import Loader
from .meta.container  import Container, Entity, Factorization, Lambda
from .meta.definition import ParameterCollection
from .wrapper         import Wrapper


def _assert_with_annotation(definition, expected_param):
    param_name       = expected_param.name
    param_annotation = expected_param.annotation

    if param_annotation != inspect._empty and not isinstance(definition, param_annotation):
        raise UnexpectedDefinitionTypeException(
            'Given {}({}), expected {}, for {}'.format(
                type(definition).__name__,
                definition,
                param_annotation.__name__,
                param_name,
            )
        )

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

        # Figure out the make method.
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

        # Compile parameters.
        known_parameters      = {}
        keyword_parameters    = {}
        positional_parameters = []

        signature        = inspect.signature(make_method)
        expected_params  = [signature.parameters[name] for name in signature.parameters]
        expected_count   = len(expected_params)

        # Check whether the signature include dynamic parameters.
        has_dynamic_positional_parameters = False
        has_dynamic_known_parameters    = False

        for param in expected_params:
            if param.kind == param.VAR_POSITIONAL:
                has_dynamic_positional_parameters = True

            if param.kind == param.VAR_KEYWORD:
                has_dynamic_known_parameters = True

        # Gather POSITIONAL OR KEYWORD parameters (predefined).
        next_fixed_index = 0

        for expected_param in expected_params:
            if expected_param.kind in (expected_param.VAR_POSITIONAL, expected_param.VAR_KEYWORD):
                continue

            if expected_param.name not in params['items']:
                # Not NULL and no default value.
                if expected_param.default and expected_param.default == inspect._empty:
                    raise MissingParameterException(
                        'Failed to initiate "{}" due to a missing parameter "{}"'.format(metadata.id, expected_param.name)
                    )

                continue

            definition = params['items'][expected_param.name]

            _assert_with_annotation(definition, expected_param)
            positional_parameters.append(definition)

            known_parameters[expected_param.name] = definition

            next_fixed_index += 1

        # Gather POSITIONAL parameters.
        for index in range(len(params['sequence'])):
            definition = params['sequence'][index]

            positional_parameters.append(definition)

            if index >= expected_count:
                if not has_dynamic_positional_parameters:
                    raise UnexpectedParameterException('Out of range: #{}'.format(index))

                continue

            expected_param = expected_params[next_fixed_index + index]

            _assert_with_annotation(definition, expected_param)

            known_parameters[expected_param.name] = definition

        # Gather KEYWORD parameters.
        for name, definition in params['items'].items():
            if name not in signature.parameters and not has_dynamic_known_parameters:
                raise UnexpectedParameterException(
                    'Failed to initiate "{}" due to an unexpected parameter "{}"'.format(metadata.id, name)
                )

            if name in known_parameters:
                # Already registered as positional parameters.

                continue

            if name in signature.parameters:
                expected_param = signature.parameters[name]

                _assert_with_annotation(definition, expected_param)

            known_parameters[name]   = definition
            keyword_parameters[name] = definition

        for expected_param in expected_params:
            param_name = expected_param.name
            param_kind = expected_param.kind

            if param_kind == expected_param.VAR_POSITIONAL and has_dynamic_positional_parameters:
                continue

            if param_kind == expected_param.VAR_KEYWORD and has_dynamic_known_parameters:
                continue

            if param_name in known_parameters:
                continue

            if expected_param.default == inspect._empty:
                if factory_service:
                    raise UndefinedDefaultValueException(
                        'Factorization: {factory_class_name}.{factory_method_name}{signature} expects the parameter "{parameter_name}" ({factory_service})'.format(
                            factory_class_name  = type(factory_service).__name__,
                            factory_method_name = factory_method_name,
                            signature           = signature,
                            parameter_name      = param_name,
                            factory_service     = str(factory_service),
                        )
                    )

                raise UndefinedDefaultValueException(
                    'Entity: {make_method_name}{signature} expects the parameter "{parameter_name}" ({make_method})'.format(
                        make_method_name  = make_method.__name__,
                        signature         = signature,
                        parameter_name    = param_name,
                        make_method       = make_method
                    )
                )

        return make_method(*positional_parameters, **keyword_parameters)

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
