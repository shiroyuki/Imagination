import contextlib

from ..meta.definition import ParameterCollection


def get_fully_qualified_class_name(cls) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"


@contextlib.contextmanager
def exclusive_lock(lock):
    """ ..deprecated:: Use the ``with`` statement instead.
    """
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

    for _, item in collection.items():
        if type(item.definition) is ParameterCollection:
            container_ids.update(
                extract_dependency_ids_from_parameters(item.definition)
            )

            continue

        if item.kind != 'entity':
            continue

        container_ids.add(item.definition)

    return container_ids
