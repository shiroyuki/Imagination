# v2
from .controller         import Controller
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
        self.__controller_map = {}
        self.__on_lockdown    = False
        self.__transformer    = Transformer(self.get)

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

        for container_id, meta_container in meta_container_map.items():
            self.set_metadata(container_id, meta_container)

    def contain(self, container_id : str):
        return container_id in self.__controller_map

    def get(self, container_id : str):
        info = self.get_info(container_id)

        if not info.activation_sequence:
            new_sequence = self._calculate_activation_sequence(container_id)
            info.activation_sequence = new_sequence

        # Activate all dependencies.
        for dependency_id in info.activation_sequence:
            self.get_info(dependency_id).activate()

        # Activate the requested container ID.
        return self.get_info(container_id).activate()

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
                                           self.__transformer.cast)

        self.__controller_map[container_id] = new_controller

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
