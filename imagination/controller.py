# v2
import inspect
import logging

from .debug           import get_logger
from .exc             import MissingParameterException, \
                             UnexpectedDefinitionTypeException
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
                 transformer_cast       : callable,
                 ):
        self.__metadata               = metadata
        self.__core_get               = core_get
        self.__core_get_interceptions = core_get_interceptions
        self.__transformer_cast       = transformer_cast
        self.__logger                 = get_logger('controller/{}'.format(metadata.id))
        self.__container_instance     = None  # Cache
        self.__wrapper_instance       = None  # Wrapper Cache
        self.__ignored_parameters     = []

        self.activation_sequence = None  # Activation Sequence

    @property
    def metadata(self):
        return self.__metadata

    @property
    def instance(self):
        return self.__wrapper_instance or self.__container_instance

    @property
    def instantiator(self):
        metadata       = self.__metadata
        container_type = type(metadata)

        if container_type is Lambda:
            return Loader(metadata.fq_callable_name).package

        if container_type is Entity:
            return Loader(metadata.fqcn).package
        elif container_type is Factorization:
            factory_service     = self.__core_get(metadata.factory_id)
            factory_method_name = metadata.factory_method_name
            return getattr(factory_service, factory_method_name)

        raise NotImplementedError('No make method for {}'.format(container_type.__name__))

    def activated(self):
        return self.__wrapper_instance is not None or self.__container_instance is not None

    def activate(self, previously_activated : list = None):
        previously_activated = previously_activated or []

        if self.activated():
            return self.__wrapper_instance or self.__container_instance

        if self.metadata.id in previously_activated:
            raise CircularDependencyError('{}: previous activation sequence: {}'.format(self.metadata.id, ', '.join(previously_activated)))

        previously_activated.append(self.metadata.id)

        new_instance = self.__instantiate_container(previously_activated)

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

    def __instantiate_container(self, previously_activated : list):
        if isinstance(self.__metadata, Lambda):
            return self.instantiator

        return self.__execute(self.instantiator,
                              self.__cast_to_params(self.__metadata.params,
                                                    previously_activated))

    def run_initial_calls(self, previously_activated : list):
        internal_instance = self.activate(previously_activated)

        for initial_call in self.__metadata.initial_calls:
            self.__execute_after_instantiation(internal_instance, initial_call.method_name, initial_call.parameters, previously_activated)

    def __execute(self, target_callable, params):
        # Compile parameters.
        signature          = inspect.signature(target_callable)
        expected_params    = [signature.parameters[name] for name in signature.parameters]
        enable_auto_wiring = self.metadata.auto_wired

        # Check whether the signature include dynamic parameters.
        self.__scan_for_dynamic_parameters(expected_params)
        parameters = self.__scan_for_usable_parameters(params, expected_params, auto_wire = enable_auto_wiring)

        return target_callable(*parameters['args'], **parameters['kwargs'])

    def __execute_after_instantiation(self, instance, method_name, params, previously_activated):
        if not hasattr(instance, method_name):
            raise AttributeError('The entity {} has no method named {}.'.format(self.__metadata.id, method_name))

        parameters = self.__cast_to_params(params, previously_activated)

        logging.debug('[Imagination/Controller] {}.{}({})'.format(
            instance,
            method_name,
            parameters,
        ))

        self.__execute(getattr(instance, method_name), parameters)

    def __scan_for_usable_parameters(self, given_params, expected_params, auto_wire:bool):
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

        self.__logger.debug('ID {}: Given: {}'.format(self.__metadata.id, given_params))

        # First, consider the keyword ones.
        # FIXME This is for backward-compatibility and the whole loop will be removed in version 3.
        for key, definition in given_params['items'].items():
            # Handle a dynamic parameter.
            if key not in fixed_parameter_map:
                self.__logger.debug('ID {}: Keyword Param ({} -> {}): Considered as extra'.format(self.__metadata.id, key, definition))

                keywoard_parameters[key] = definition

                continue

            self.__logger.debug('ID {}: Keyword Param ({} -> {}): Considered as defined'.format(self.__metadata.id, key, definition))

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
                self.__logger.debug('ID {}: Positional Param ({}): Considered as extra'.format(self.__metadata.id, definition))

                positional_parameters.append(definition)

                continue

            fixed_parameter = fixed_parameter_list[iterating_index]

            # Handle a defined parameter.
            # FIXME This is for backward-compatibility and this block will be removed in version 3.
            if fixed_parameter.defined:
                self.__logger.debug('ID {}: Positional Param ({}): Backward compatible'.format(self.__metadata.id, definition))

                positional_parameters.append(definition)

                continue

            self.__logger.debug('ID {}: Positional Param ({}): Considered as defined'.format(self.__metadata.id, definition))

            fixed_parameter.defined     = True
            fixed_parameter.value       = definition
            fixed_parameter.source_type = list
            fixed_parameter.source_ref  = iterating_index

            iterating_index += 1

        # Check for missing parameters or wrong parameter specification.
        undefined_fixed_parameter_count = len(fixed_parameter_list)
        undefined_parameters            = []

        auto_wiring_count = 0

        for fixed_parameter in fixed_parameter_list:
            _assert_with_annotation(self.__metadata.id, fixed_parameter)

            if fixed_parameter.defined:
                self.__logger.debug('ID {}: Param {}: Already defined'.format(self.__metadata.id, fixed_parameter.name))

                continue

            if not fixed_parameter.required:
                self.__logger.debug('ID {}: Param {}: Delegated'.format(self.__metadata.id, fixed_parameter.name))

                undefined_fixed_parameter_count -= 1

                continue

            self.__logger.debug('ID {}: Param {}: Not defined'.format(self.__metadata.id, fixed_parameter.name))

            feature_info_list = ['pos: {}'.format(fixed_parameter.index)]

            if fixed_parameter.spec.annotation != inspect._empty:
                annotation = fixed_parameter.spec.annotation

                feature_info_list.append('spec: {}'.format(annotation))

                if not issubclass(annotation, (int, float, bytes, bool, str, complex, set, dict, list, tuple)):
                    if auto_wire:  # Attempt to automatically wire a missing dependency.
                        auto_wiring_count += 1
                        given_params['items'][fixed_parameter.name] = self.__core_get(annotation)
                    else:
                        feature_info_list.append('ignored: auto-wire')

            undefined_parameters.append('{} ({})'.format(fixed_parameter.name, ', '.join(feature_info_list)))

        # Double-check the parameters after rewiring dependencies.
        if auto_wire and auto_wiring_count > 0:
            return self.__scan_for_usable_parameters(given_params, expected_params, auto_wire=False)

        if undefined_parameters:
            raise MissingParameterException(
                'Entity {}: Missing Parameters: {}'.format(self.__metadata.id, ', '.join(undefined_parameters))
            )

        # When NOT all fixed parameters are defined, all additional positional parameters will be disregarded.
        if undefined_fixed_parameter_count > 0:
            kwargs = {key: metadata.value for key, metadata in fixed_parameter_map.items() if metadata.defined}
            kwargs.update(keywoard_parameters)

            logging.info('Not all fixed parameters defined. All positional parameters will be ignored.')

            return {
                'args'   : [],
                'kwargs' : kwargs,
            }

        # When all fixed parameters are defined, they will be converted into positional parameters.
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

    def __cast_to_params(self, params : ParameterCollection, previously_activated : list):
        sequence = []
        items    = {}

        for item in params.sequence():
            try:
                sequence.append(self.__transformer_cast(item, previously_activated))
            except TypeError:
                raise ValueInterpretationError('Entity "{}": Failed to interpret {} (positional)'.format(self.__metadata.id, item))

        for key, value in params.items():
            try:
                items[key] = self.__transformer_cast(value, previously_activated)
            except TypeError:
                raise ValueInterpretationError('Entity "{}": Failed to interpret "{}" -> {} (keyword)'.format(self.__metadata.id, key, value))

        return {
            'sequence' : sequence,
            'items'    : items,
        }


class CircularDependencyError(RuntimeError):
    """ Circular Dependency Error """


class ValueInterpretationError(RuntimeError):
    """ Value interpretation error """


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
