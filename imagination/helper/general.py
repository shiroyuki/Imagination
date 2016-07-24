from ..meta.definition import ParameterCollection

def extract_container_ids_from_parameter_collection(collection):
    container_ids = set()

    for item in collection.sequence():
        if type(item.definition) is ParameterCollection:
            container_ids.update(
                extract_container_ids_from_parameter_collection(item.definition)
            )

            continue

        if item.kind != 'entity':
            continue

        container_ids.add(item.definition)

    for k, item in collection.items():
        if type(item.definition) is ParameterCollection:
            container_ids.update(
                extract_container_ids_from_parameter_collection(item.definition)
            )

            continue

        if item.kind != 'entity':
            continue

        container_ids.add(item.definition)

    return container_ids
