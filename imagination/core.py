# v2
from contextlib import contextmanager
import threading
from typing import Callable, Optional
import uuid

from .controller         import Controller
from .debug              import get_logger
from .exc                import UndefinedContainerIDError
from .helper.context     import DefinitionContext
from .helper.general     import exclusive_lock
from .helper.id_naming   import fully_qualified_class_name as default_id_naming_strategy
from .helper.transformer import Transformer
from .meta.container     import Container, Entity, Factorization, Lambda
from .meta.definition    import MethodCall

CORE_SELF_REFERENCE = 'container'
log = get_logger(__name__)


class CoreOnLockDownError(RuntimeError):
    """ Error when the external code attempts to update the
        map of container metadata.
    """


class Imagination(object):
    """ Imagination Core

        In order to track the interceptions properly, the code will keep all
        information in ``self.__interception_graph``, which is a tree where::

            container-id
            (1) --> (0..n) method name
                            (1) --> (3) event-type
                                        (1) --> (0..n) interception

    """
    def __init__(self, transformer: Transformer = None, standalone_mode: bool = False):
        self.__guid = uuid.uuid4()

        self.__standalone_mode = standalone_mode

        self.__internal_lock  = threading.Lock()
        self.__controller_map = {}
        self.__on_lockdown    = False
        self.__transformer    = transformer or Transformer(self.get)

        self.__interception_graph = {}
        self.__initial_calls      = {}

        # When this property is set, this container will only work as a proxy to
        # the other container.
        self.__original_container = None

    @property
    def guid(self):
        return self.__guid

    @property
    def original_container(self):
        return self.__original_container

    def in_standalone_mode(self):
        return self.__standalone_mode

    def in_proxy_mode(self):
        return bool(self.__original_container)

    def act_as(self, other):
        assert other.guid != self.guid, 'The other container must not be itself.'
        assert not other.in_proxy_mode(), 'The other container must not be in the proxy mode.'

        self.__original_container = other

    def stop_proxy_mode(self):
        self.__original_container = None

    def lock_down(self):
        """ Lock down the core.

            This will prevent the core from accepting new entity definition.

            .. note:: This method will be invoked on the first ``get`` call.
        """
        log.debug(f'Lock down the container.')
        self.__on_lockdown = True

    def is_on_lockdown(self) -> bool:
        """ Check if the core is locked down. """
        return self.__on_lockdown

    def update_metadata(self, meta_container_map : dict):
        """ Batch update the metadata map.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            if self.__standalone_mode:
                log.info('Core appears to be on lockdown but the standalone'
                         ' mode will allow the attempt to batch-update the'
                         ' meta container map.')
            else:
                raise CoreOnLockDownError('Failed to batch-update the meta container map')

        with exclusive_lock(self.__internal_lock):
            for entity_id, meta_container in meta_container_map.items():
                self.set_metadata(entity_id, meta_container)

    def contain(self, entity_id : str):
        """ Check if the entity ID is registered.

            This is compatible with the proxy mode.
        """
        if self.original_container:
            return self.original_container.contain(entity_id)

        return entity_id in self.__controller_map

    def get(self, entity_id, previously_activated : list = None, id_naming_strategy : Optional[Callable] = None,
            lock_down_enabled: bool = True):
        """ Retrieve an entity by ID

            :param entity_id: the identifier of the entity or a class of the service.
            :param list previously_activated: the list of identifiers of previously activated entities (for internal use only)
            :param Callable id_naming_strategy: an optional callable object for ID naming strategy
            :param bool lock_down_enabled: the flag to enable the core lockdown

            When :param:`entity_id` is a class of the service, it would use the default ID naming strategy to refer to the service of the same class.

            This is compatible with the proxy mode.
        """
        global CORE_SELF_REFERENCE

        # NOTE: Assume non-string ``entity_id`` to be a class.
        actual_entity_id = (entity_id
                            if isinstance(entity_id, str)
                            else (id_naming_strategy or default_id_naming_strategy)(entity_id))

        if self.original_container:
            return self.original_container.get(entity_id)

        if actual_entity_id == CORE_SELF_REFERENCE:
            return self

        info = self.get_info(actual_entity_id)

        if info.activated():
            return info.instance

        # with exclusive_lock(self.__internal_lock):
        # On the first request, the core will be on lockdown.
        if not self.is_on_lockdown():
            if lock_down_enabled:
                self.lock_down()
            self._declare_initial_method_calls()
            self._generate_interception_graph()

        if not info.activation_sequence:
            new_sequence = self._calculate_activation_sequence(actual_entity_id)

            info.activation_sequence = new_sequence

        previously_activated = previously_activated or []
        activation_sequence  = []

        # Activate all dependencies.
        for dependency_id in info.activation_sequence:
            if dependency_id == CORE_SELF_REFERENCE:
                continue

            # Trigger the service activation.
            self.get_info(dependency_id).activate(previously_activated)

            activation_sequence.append(dependency_id)

        # Activate the requested container ID.
        instance = info.activate()

        activation_sequence.append(actual_entity_id)

        for activated_entity_id in activation_sequence:
            self.get_info(activated_entity_id).run_initial_calls(previously_activated)

        return instance

    def all_ids(self):
        """ Get all entity IDs.

            :rtype: tuple

            This is compatible with the proxy mode.
        """
        if self.original_container:
            return self.original_container.all_ids()

        return tuple(self.__controller_map.keys())

    def get_info(self, entity_id : str) -> Controller:
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        if not self.contain(entity_id):
            raise UndefinedContainerIDError(entity_id)

        return self.__controller_map[entity_id]

    def get_metadata(self, entity_id : str) -> Container:
        """ Retrieve the metadata of the container.

            This is compatible with the proxy mode.
        """
        if self.original_container:
            return self.original_container.get_metadata(entity_id)

        return self.get_info(entity_id).metadata

    def set_metadata(self, entity_id : str, new_meta_container : Container):
        """ Define the metadata of the new container.

            .. warning:: This method allows ID overriding.
            .. warning:: Use this with care.
        """
        log.debug(f'Set metadata for {entity_id}')

        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        if self.__on_lockdown:
            if self.__standalone_mode and entity_id not in self.__controller_map:
                log.info('The container appears to be on lockdown but the standalone'
                         f' mode will allow the container to define entity {entity_id}.')
            else:
                raise CoreOnLockDownError(
                    f'Failed to set the metadata for an entity {entity_id}'
                    if self.__standalone_mode
                    else 'The container is already on lockdown and blocks any'
                         f' update to the metadata of entity {entity_id}.'
                )

        # Redefine the container ID.
        new_meta_container.id = entity_id
        new_controller        = Controller(new_meta_container,
                                           self.get,
                                           self.get_interceptions,
                                           self.__transformer.cast)

        self.__controller_map[entity_id] = new_controller

    def get_interceptions(self, intercepted_id, event_type = None,
                          method_to_intercept = None):
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        if intercepted_id not in self.__interception_graph:
            return None

        sub_graph = self.__interception_graph[intercepted_id]

        if not (event_type and method_to_intercept):
            return sub_graph

        if event_type and not method_to_intercept:
            return sub_graph[event_type]

        if not event_type and method_to_intercept:
            raise ValueError('The event type must be defined.')

        return sub_graph[event_type][method_to_intercept]

    def set_initial_call(self, method_call : MethodCall):
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        target_id = method_call.actor_id

        if not isinstance(method_call, MethodCall):
            raise ValueError('The definition for the initial method call is not properly defined.')

        if not (method_call.actor_id and method_call.method_name):
            raise ValueError('The definition for the initial method call is invalid.')

        if target_id not in self.__initial_calls:
            self.__initial_calls[target_id] = []

        self.__initial_calls[target_id].append(method_call)

    @contextmanager
    def define_entity(self, entity_id, fqcn):
        """ Define a new entity. """
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        container = Entity(identifier = entity_id, fqcn = fqcn)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextmanager
    def define_factorization(self, entity_id, factory_id, factory_method_name):
        """ Define a new entity with factorization. """
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        container = Factorization(entity_id, factory_id, factory_method_name)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextmanager
    def define_lambda(self, entity_id, import_path):
        """ Define a new lambda definition. """
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        container = Lambda(entity_id, import_path)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextmanager
    def update_definition(self, entity_id):
        """ Update the existing definition. """
        if self.original_container:
            raise RuntimeWarning('This method is disabled when the container is running in the proxy mode.')

        yield DefinitionContext(self, self.get_metadata(entity_id))

    def reset(self):
        for ctrl in list(self.__controller_map.keys()):
            del self.__controller_map[ctrl]

    def _calculate_activation_sequence(self, entity_id, known_activation_sequence = None):
        global CORE_SELF_REFERENCE

        if entity_id == CORE_SELF_REFERENCE:
            return []

        known_activation_sequence = known_activation_sequence or []

        # To prevent infinite loop
        if entity_id in known_activation_sequence:
            return []

        scoreboard = {}  # id -> number of dependants

        known_activation_sequence.append(entity_id)

        metadata = self.get_metadata(entity_id)

        for dependency_id in metadata.dependencies:
            # To prevent infinite loop
            if dependency_id in known_activation_sequence:
                continue

            if dependency_id not in scoreboard:
                scoreboard[dependency_id] = 0

            scoreboard[dependency_id] += 1

            additionals = self._calculate_activation_sequence(dependency_id, known_activation_sequence)

            for additional_dependency_id in additionals:
                if additional_dependency_id not in scoreboard:
                    scoreboard[additional_dependency_id] = 0

                scoreboard[additional_dependency_id] += 1

        sorted_sequence = [
            (dependency_id, score)
            for dependency_id, score in scoreboard.items()
        ]

        sorted_sequence.sort(key = lambda step: step[1])

        return [
            step[0]
            for step in sorted_sequence
        ]

    def _generate_interception_graph(self):
        interception_graph   = self.__interception_graph
        unique_interceptions = list()

        for controller in self.__controller_map.values():
            metadata = controller.metadata

            unique_interceptions.extend(
                interception
                for interception in metadata.interceptions
                if interception not in unique_interceptions
            )

        for interception in unique_interceptions:
            event_type         = interception.when_to_intercept
            intercepted_id     = interception.intercepted_id
            intercepted_method = interception.method_to_intercept

            if intercepted_id not in interception_graph:
                interception_graph[intercepted_id] = {}

            method_to_event_map = interception_graph[intercepted_id]

            if intercepted_method not in method_to_event_map:
                method_to_event_map[intercepted_method] = {
                    'after'  : [],
                    'before' : [],
                    'error'  : [],
                }

            method_to_event_map[intercepted_method][event_type].append(interception)

    def _declare_initial_method_calls(self):
        for controller in self.__controller_map.values():
            metadata = controller.metadata

            if metadata.id not in self.__initial_calls:
                continue

            metadata.initial_calls.extend(self.__initial_calls[metadata.id])
