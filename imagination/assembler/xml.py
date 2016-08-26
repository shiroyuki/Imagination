# v2
import re

from kotoba import load_from_file

from ..meta.container  import Container
from ..meta.definition import ParameterCollection, DataDefinition, Interception
from .abstract         import ConfigParser
from .handlers         import EntityCreator, FactorizationCreator, LambdaCreator


__re_factorization_element_name = re.compile('^factori(s|z)ation$')
__container_creators            = [EntityCreator, FactorizationCreator, LambdaCreator]


class UnsupportedContainerError(RuntimeError):
    """ Error when an unsupported container is defined. """


class UnknownEventTypeError(RuntimeError):
    """ Error when an unknown event type is spotted. """


def convert_container_node_to_meta_container(container_node) -> Container:
    container_type   = container_node.name().lower()
    container_id     = container_node.attribute('id')
    container_params = convert_container_node_to_parameter_collection(container_node)
    interceptions    = convert_blocks_to_interception_metadatas(container_node)

    for creator in __container_creators:
        if not creator.can_handle(container_type):
            continue

        return creator.create(container_id, container_params,
                              interceptions, container_node)

    raise UnsupportedContainerError(container_type)


def convert_container_node_to_parameter_collection(node, key_property_name = None) -> ParameterCollection:
    collection = ParameterCollection()

    for child_node in node.children():
        if child_node.name() not in ('param', 'item'):
            continue

        name = child_node.attribute(key_property_name or 'name') or None
        kind = child_node.attribute('type')

        definition = convert_container_node_to_parameter_collection(child_node, 'key') \
            if kind in ('tuple', 'list', 'dict') \
            else child_node.data().strip()

        data = DataDefinition(definition, name, kind)

        collection.add(data, name)

    return collection


def convert_blocks_to_interception_metadatas(node):
    interceptor_id = node.attribute('id')
    interceptions  = []

    for child_node in node.children('interception'):
        event_type          = None
        intercepted_id      = None
        method_to_intercept = child_node.attribute('do')
        intercepting_method = child_node.attribute('with')

        for known_event_type in Interception.__known_events__:
            if child_node.attribute(known_event_type):
                event_type     = known_event_type
                intercepted_id = child_node.attribute(event_type)

                break

        try:
            interceptions.append(Interception(
                when_to_intercept   = event_type,
                intercepted_id      = intercepted_id,
                method_to_intercept = method_to_intercept,
                interceptor_id      = interceptor_id,
                intercepting_method = intercepting_method,
            ))
        except AssertionError as e:
            raise UnknownEventTypeError(
                'Invalid Interception for {} ({})'.format(
                    node.attribute('id'),
                    e
                )
            )

    return interceptions


class XMLParser(ConfigParser):
    def __init__(self):
        self._re_acceptable_file_extension = re.compile('\.xml$', re.IGNORECASE)

    def can_handle(self, filepath : str):
        return bool(self._re_acceptable_file_extension.search(filepath))

    def parse(self, filepath : str):
        root_node     = load_from_file(filepath)
        container_map = {}

        for container_node in root_node.children():
            meta_container = convert_container_node_to_meta_container(container_node)

            container_map[meta_container.id] = meta_container

        return container_map
