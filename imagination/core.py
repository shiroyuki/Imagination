# v2
import contextlib
import threading

from .controller         import Controller
from .exc                import UndefinedContainerIDError
from .helper.context     import DefinitionContext
from .helper.general     import exclusive_lock
from .helper.transformer import Transformer
from .meta.container     import Container, Entity, Factorization, Lambda
from .meta.definition    import MethodCall

CORE_SELF_REFERENCE = 'container'


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
    def __init__(self, transformer : Transformer = None):
        self.__internal_lock  = threading.Lock()
        self.__controller_map = {}
        self.__on_lockdown    = False
        self.__transformer    = transformer or Transformer(self.get)

        self.__interception_graph = {}
        self.__initial_calls      = {}

    def lock_down(self):
        """ Lock down the core.

            This will prevent the core from accepting new entity definition.

            .. note:: This method will be invoked on the first ``get`` call.
        """
        self.__on_lockdown = True

    def is_on_lockdown(self) -> bool:
        """ Check if the core is locked down. """
        return self.__on_lockdown

    def update_metadata(self, meta_container_map : dict):
        """ Batch update the metadata map.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError()

        with exclusive_lock(self.__internal_lock):
            for entity_id, meta_container in meta_container_map.items():
                self.set_metadata(entity_id, meta_container)

    def contain(self, entity_id : str):
        """ Check if the entity ID is registered. """
        return entity_id in self.__controller_map

    def get(self, entity_id : str, previously_activated : list = None):
        """ Retrieve an entity by ID

            :param str entity_id: the identifier of the entity
            :param list previously_activated: the list of identifiers of previously activated entities (for internal use only)
        """
        global CORE_SELF_REFERENCE

        if entity_id == CORE_SELF_REFERENCE:
            return self

        info = self.get_info(entity_id)

        if info.activated():
            return info.instance

        # with exclusive_lock(self.__internal_lock):
        # On the first request, the core will be on lockdown.
        if not self.is_on_lockdown():
            self.lock_down()
            self._declare_initial_method_calls()
            self._generate_interception_graph()

        if not info.activation_sequence:
            new_sequence = self._calculate_activation_sequence(entity_id)

            info.activation_sequence = new_sequence

        previously_activated = previously_activated or []
        activation_sequence  = []

        # Activate all dependencies.
        for dependency_id in info.activation_sequence:
            if dependency_id == CORE_SELF_REFERENCE:
                continue

            dependency = self.get_info(dependency_id).activate(previously_activated)

            activation_sequence.append(dependency_id)

        # Activate the requested container ID.
        instance = info.activate()

        activation_sequence.append(entity_id)

        for activated_entity_id in activation_sequence:
            self.get_info(activated_entity_id).run_initial_calls(previously_activated)

        return instance

    def all_ids(self):
        """ Get all entity IDs.

            :rtype: tuple
        """
        return tuple(self.__controller_map.keys())

    def get_info(self, entity_id : str) -> Controller:
        if not self.contain(entity_id):
            raise UndefinedContainerIDError(entity_id)

        return self.__controller_map[entity_id]

    def get_metadata(self, entity_id : str) -> Container:
        """ Retrieve the metadata of the container. """
        return self.get_info(entity_id).metadata

    def set_metadata(self, entity_id : str, new_meta_container : Container):
        """ Define the metadata of the new container.

            .. warning:: This method allows ID overriding.
            .. warning:: Use this with care.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError()

        # Redefine the container ID.
        new_meta_container.id = entity_id
        new_controller        = Controller(new_meta_container,
                                           self.get,
                                           self.get_interceptions,
                                           self.__transformer.cast)

        self.__controller_map[entity_id] = new_controller

    def get_interceptions(self, intercepted_id, event_type = None,
                          method_to_intercept = None):
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
        target_id = method_call.actor_id

        if not isinstance(method_call, MethodCall):
            raise ValueError('The definition for the initial method call is not properly defined.')

        if not (method_call.actor_id and method_call.method_name):
            raise ValueError('The definition for the initial method call is invalid.')

        if target_id not in self.__initial_calls:
            self.__initial_calls[target_id] = []

        self.__initial_calls[target_id].append(method_call)

    @contextlib.contextmanager
    def define_entity(self, entity_id, fqcn):
        """ Define a new entity. """
        container = Entity(identifier = entity_id, fqcn = fqcn)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextlib.contextmanager
    def define_factorization(self, entity_id, factory_id, factory_method_name):
        """ Define a new entity with factorization. """
        container = Factorization(entity_id, factory_id, factory_method_name)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextlib.contextmanager
    def define_lambda(self, entity_id, import_path):
        """ Define a new lambda definition. """
        container = Lambda(entity_id, import_path)

        self.update_metadata({entity_id: container})

        yield DefinitionContext(self, container)

    @contextlib.contextmanager
    def update_definition(self, entity_id):
        yield DefinitionContext(self, self.get_metadata(entity_id))

    def _calculate_activation_sequence(self, entity_id, known_activation_sequence = None):
        global CORE_SELF_REFERENCE

        if entity_id == CORE_SELF_REFERENCE:
            return []

        known_activation_sequence = known_activation_sequence or []

        # To prevent infinite loop
        if entity_id in known_activation_sequence:
            return []

        activation_sequence = []
        scoreboard          = {}  # id -> number of dependants

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

        for entity_id, controller in self.__controller_map.items():
            metadata = controller.metadata

            for interception in metadata.interceptions:
                if interception in unique_interceptions:
                    continue

                unique_interceptions.append(interception)

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
        for entity_id, controller in self.__controller_map.items():
            metadata = controller.metadata

            if metadata.id not in self.__initial_calls:
                continue

            metadata.initial_calls.extend(self.__initial_calls[metadata.id])
