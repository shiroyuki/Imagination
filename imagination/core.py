class UndefinedContainerIDError(RuntimeError):
    """ Error when an undefined container ID is requested. """

class Imagination(object):
    def __init__(self):
        self._meta_container_map = {}

    def update_metadata(self, meta_container_map : dict):
        self._meta_container_map.update(meta_container_map)

    def contain(self, container_id : str):
        return container_id in self._meta_container_map

    def get(self, container_id : str):
        if not self.contain(self, container_id):
            raise UndefinedContainerIDError(container_id)

        # TODO activate all depdendencies.
        # TODO activate the requested container ID.

        raise NotImplemented('WIP')
