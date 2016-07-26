# v2
import re

from kotoba import load_from_file

from ..meta.container  import Entity, Factorization
from ..meta.definition import ParameterCollection, DataDefinition
from .abstract         import ConfigParser


__re_factorization_element_name = re.compile('^factori(s|z)ation$')


def convert_container_node_to_meta_container(container_node) -> Entity:
    container_type = container_node.name()

    if container_type == 'entity':
        return Entity(
            container_node.attribute('id'),
            container_node.attribute('class') or None,
            convert_container_node_to_parameter_collection(container_node)
        )

    if __re_factorization_element_name.search(container_type):
        return Factorization(
            container_node.attribute('id'),
            container_node.attribute('with'),
            container_node.attribute('call'),
            convert_container_node_to_parameter_collection(container_node)
        )

    raise NotImplementedError()


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
