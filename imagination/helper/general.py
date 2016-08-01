import contextlib

from ..meta.definition import ParameterCollection


@contextlib.contextmanager
def exclusive_lock(lock):
    lock.acquire()
    yield
    lock.release()


def extract_dependency_ids_from_parameters(collection : ParameterCollection):
    container_ids = set()

    for item in collection.sequence():
        if type(item.definition) is ParameterCollection:
            container_ids.update(
                extract_dependency_ids_from_parameters(item.definition)
            )

            continue

        if item.kind != 'entity':
            continue

        container_ids.add(item.definition)

    for k, item in collection.items():
        if type(item.definition) is ParameterCollection:
            container_ids.update(
                extract_dependency_ids_from_parameters(item.definition)
            )

            continue

        if item.kind != 'entity':
            continue

        container_ids.add(item.definition)

    return container_ids
