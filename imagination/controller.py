# v2
import inspect
import logging

from .debug           import get_logger, dump_meta_container
from .exc             import UnexpectedParameterException, MissingParameterException, \
                             UnexpectedDefinitionTypeException, DuplicateKeyError
from .loader          import Loader
from .meta.container  import Container, Entity, Factorization, Lambda
from .meta.definition import ParameterCollection
from .wrapper         import Wrapper


def _assert_with_annotation(entity_id, metadata):
    definition       = metadata.value
    param_name       = metadata.spec.name
    param_annotation = metadata.spec.annotation

    if isinstance(definition, Undefined):
        # No assertion on undefined definition.

        return

    try:
        if param_annotation != inspect._empty and not isinstance(definition, param_annotation):
            raise UnexpectedDefinitionTypeException(
                '{}: Given {}({}), expected {}, for {}'.format(
                    entity_id,
                    type(definition).__name__,
                    definition,
                    param_annotation.__name__,
                    param_name,
                )
            )
    except TypeError:
        # For now, bypass the error when `param_annotation` is `callable`.
        # FIXME properly handle bad annotation

        pass

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
        self.__ignored_parameters     = []
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
        signature        = inspect.signature(make_method)
        expected_params  = [signature.parameters[name] for name in signature.parameters]

        # Check whether the signature include dynamic parameters.
        self.__scan_for_dynamic_parameters(expected_params)
        parameters = self.__scan_for_usable_parameters(params, expected_params)

        return make_method(*parameters['args'], **parameters['kwargs'])

    def __scan_for_usable_parameters(self, given_params, expected_params):
        fixed_parameter_list  = []
        fixed_parameter_map   = {}
        fixed_parameter_count = 0
        positional_parameters = []
        keywoard_parameters   = {}
        iterating_index       = 0

        for expected_param in expected_params:
            if expected_param.name in self.__ignored_parameters:
                continue

            parameter_name     = expected_param.name
            parameter_required = expected_param.default and expected_param.default == inspect._empty
            parameter_metadata = ParameterMetadata(iterating_index, parameter_name, parameter_required, expected_param)

            fixed_parameter_map[parameter_name] = parameter_metadata

            fixed_parameter_list.append(parameter_metadata)

            iterating_index += 1

        fixed_parameter_count = iterating_index

        # Gather definitions from the given parameters.
        iterating_index = 0 # reset the index

        # First, consider the keyword ones.
        # FIXME This is for backward-compatibility and the whole loop will be removed in version 3.
        for key, definition in given_params['items'].items():
            # Handle a dynamic parameter.
            if key not in fixed_parameter_map:
                keywoard_parameters[key] = definition

                continue

            fixed_parameter = fixed_parameter_map[key]

            fixed_parameter.defined     = True
            fixed_parameter.value       = definition
            fixed_parameter.source_type = dict
            fixed_parameter.source_ref  = key

        # Consider the positional ones.
        # NOTE default start for version 3
        for definition in given_params['sequence']:
            # Handle a dynamic parameter.
            if iterating_index >= fixed_parameter_count:
                positional_parameters.append(definition)

                continue

            fixed_parameter = fixed_parameter_list[iterating_index]

            # Handle a defined parameter.
            # FIXME This is for backward-compatibility and this block will be removed in version 3.
            if fixed_parameter.defined:
                positional_parameters.append(definition)

                continue

            fixed_parameter.defined     = True
            fixed_parameter.value       = definition
            fixed_parameter.source_type = list
            fixed_parameter.source_ref  = iterating_index

            iterating_index += 1

        # Finally, re-consider the keyword ones.
        # FIXME Used in version 3
        # for key, definition in given_params['items'].items():
        #     # Handle a dynamic parameter.
        #     if key not in fixed_parameter_map:
        #         if key in keywoard_parameters:
        #             raise DuplicateKeyError('Entity {}: Keyword Parameter {}: Already defined'.format(self.__metadata.id, key))
        #
        #         keywoard_parameters[key] = definition
        #
        #         continue
        #
        #     fixed_parameter = fixed_parameter_map[key]
        #
        #     if fixed_parameter.defined:
        #         raise DuplicateKeyError('Entity {}: Fixed Parameter {}: Already defined'.format(self.__metadata.id, fixed_parameter.name))
        #
        #     fixed_parameter.defined     = True
        #     fixed_parameter.value       = definition
        #     fixed_parameter.source_type = dict
        #     fixed_parameter.source_ref  = key

        # Check for missing parameters or wrong parameter specification.
        undefined_parameters = []

        for fixed_parameter in fixed_parameter_list:
            _assert_with_annotation(self.__metadata.id, fixed_parameter)

            if fixed_parameter.defined or not fixed_parameter.required:
                continue

            undefined_parameters.append('{} (position {})'.format(fixed_parameter.name, fixed_parameter.index))

        if undefined_parameters:
            raise MissingParameterException(
                'Entity {}: Missing Parameters: {}'.format(self.__metadata.id, ', '.join(undefined_parameters))
            )

        # Re-assemble parameters
        args = [parameter.value for parameter in fixed_parameter_list if parameter.defined]
        args.extend(positional_parameters)

        return {
            'args'   : args,
            'kwargs' : keywoard_parameters,
        }

    def __scan_for_dynamic_parameters(self, expected_params):
        for param in expected_params:
            if param.kind == param.VAR_POSITIONAL:
                self.__ignored_parameters.append(param.name)

            if param.kind == param.VAR_KEYWORD:
                self.__ignored_parameters.append(param.name)

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


class Undefined(object):
    """ Undefined definition """


class ParameterMetadata(object):
    def __init__(self, index, name, required, spec):
        self.index       = index
        self.name        = name
        self.required    = required
        self.spec        = spec
        self.value       = Undefined()
        self.defined     = False
        self.source_type = None # list or dict
        self.source_ref  = None # index (list) or key (dict)
