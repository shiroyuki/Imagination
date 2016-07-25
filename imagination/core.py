# v2
from .meta.container import Container


class UndefinedContainerIDError(RuntimeError):
    """ Error when an undefined container ID is requested. """

class CoreOnLockDownError(RuntimeError):
    """ Error when the external code attempts to update the map of container metadata """

class ContainerInfo(object):
    def __init__(self, metadata):
        self.metadata = metadata

        self.container_instance  = None # Cache
        self.activation_sequence = None # Activation Sequence

    def activated(self):
        return self.container_instance is not None

class Imagination(object):
    def __init__(self):
        self.__container_info_map = {}
        self.__on_lockdown        = False

    def lock_down(self):
        self.__on_lockdown = True

    def is_on_lockdown(self) -> bool:
        return self.__on_lockdown

    def update_metadata(self, meta_container_map : dict):
        """ Batch update the metadata map.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError('Blocked the attempt to define multiple objects')

        for container_id, meta_container in meta_container_map.items():
            self.set_metadata(container_id, meta_container)

    def contain(self, container_id : str):
        return container_id in self.__container_info_map

    def get(self, container_id : str):
        info = self.get_info(container_id)

        if not info.activation_sequence:
            info.activation_sequence = self._calculate_activation_sequence(container_id)

        # Activate all dependencies.
        for dependency_id in info.activation_sequence:
            self._activate_container(dependency_id)

        # Activate the requested container ID.
        return self._activate_container(container_id)

    def get_info(self, container_id : str) -> ContainerInfo:
        if not self.contain(container_id):
            raise UndefinedContainerIDError(container_id)

        return self.__container_info_map[container_id]

    def get_metadata(self, container_id : str) -> Container:
        return self.get_info(container_id).metadata

    def set_metadata(self, container_id : str, new_meta_container : Container):
        """ Define the metadata of the new container.

            .. warning:: This method allows ID overriding.
        """
        if self.__on_lockdown:
            raise CoreOnLockDownError('Blocked the attempt to define the container identified as {}'.format(container_id))

        # Redefine the container ID.
        new_meta_container.id = container_id

        self.__container_info_map[container_id] = ContainerInfo(new_meta_container)

    def _activate_container(self, container_id):
        info = self.get_info(container_id)

        # If there is the cache of the container, return it.
        if info.activated():
            return info.container_instance

        container_instance = None
        raise NotImplementedError('WIP: Implement the instantiation logic from the metadata.')

        if info.metadata.cacheable:
            info.container_instance = container_instance

        return container_instance

    def _calculate_activation_sequence(self, container_id):
        activation_sequence = []
        scoreboard = {} # id -> number of dependants

        metadata = self.get_metadata(container_id)

        for dependency_id in metadata.dependencies:
            if dependency_id not in scoreboard:
                scoreboard[dependency_id] = 0

            scoreboard[dependency_id] += 1

            additional_dependencies = self._calculate_activation_sequence(dependency_id)

            for additional_dependency_id in additional_dependencies:
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
