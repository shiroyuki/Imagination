# v2
import pprint
import threading

from .controller         import Controller
from .helper.general     import exclusive_lock
from .helper.transformer import Transformer
from .meta.container     import Container


class UndefinedContainerIDError(RuntimeError):
    """ Error when an undefined container ID is requested. """


class CoreOnLockDownError(RuntimeError):
    """ Error when the external code attempts to update the
        map of container metadata.
    """


class Imagination(object):
    def __init__(self, transformer : Transformer = None):
        self.__internal_lock  = threading.Lock()
        self.__controller_map = {}
        self.__on_lockdown    = False
        self.__transformer    = Transformer(self.get)

        self.__interception_graph = {}

    def lock_down(self):
        self.__on_lockdown = True

    def is_on_lockdown(self) -> bool:
        return self.__on_lockdown

    def update_metadata(self, meta_container_map : dict):
        """ Batch update the metadata map.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError()

        with exclusive_lock(self.__internal_lock):
            for container_id, meta_container in meta_container_map.items():
                self.set_metadata(container_id, meta_container)

    def contain(self, container_id : str):
        return container_id in self.__controller_map

    def get(self, container_id : str):
        info = self.get_info(container_id)

        with exclusive_lock(self.__internal_lock):
            # On the first request, the core will be on lockdown.
            if not self.is_on_lockdown():
                self.lock_down()
                self._generate_interception_graph()

            if not info.activation_sequence:
                new_sequence = self._calculate_activation_sequence(container_id)
                info.activation_sequence = new_sequence

        # Activate all dependencies.
        for dependency_id in info.activation_sequence:
            self.get_info(dependency_id).activate()

        # Activate the requested container ID.
        instance = self.get_info(container_id).activate()

        return instance

    def get_info(self, container_id : str) -> Controller:
        if not self.contain(container_id):
            raise UndefinedContainerIDError(container_id)

        return self.__controller_map[container_id]

    def get_metadata(self, container_id : str) -> Container:
        return self.get_info(container_id).metadata

    def set_metadata(self, container_id : str, new_meta_container : Container):
        """ Define the metadata of the new container.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError()

        # Redefine the container ID.
        new_meta_container.id = container_id
        new_controller        = Controller(new_meta_container,
                                           self.get,
                                           self.get_interceptions,
                                           self.__transformer.cast)

        self.__controller_map[container_id] = new_controller

    def get_interceptions(self, intercepted_id, event_type = None, method_to_intercept = None):
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

    def _calculate_activation_sequence(self, container_id):
        activation_sequence = []
        scoreboard          = {}  # id -> number of dependants

        metadata = self.get_metadata(container_id)

        for dependency_id in metadata.dependencies:
            if dependency_id not in scoreboard:
                scoreboard[dependency_id] = 0

            scoreboard[dependency_id] += 1

            additionals = self._calculate_activation_sequence(dependency_id)

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

        for container_id, controller in self.__controller_map.items():
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

            event_to_methods_map = interception_graph[intercepted_id]

            if event_type not in event_to_methods_map:
                event_to_methods_map[event_type] = {
                    'after'  : [],
                    'before' : [],
                    'error'  : [],
                }

            interceptions_map = event_to_methods_map[event_type]

            if intercepted_method not in interceptions_map:
                interceptions_map[intercepted_method] = []

            interceptions_map[intercepted_method].append(interception)
