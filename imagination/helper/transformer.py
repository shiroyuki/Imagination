# v2
import logging

from ..debug           import get_logger
from ..meta.definition import DataDefinition
from ..loader          import Loader


class Transformer(object):
    """ Data transformer """
    def __init__(self, core_getter : callable):
        self.__core_getter = core_getter

    def cast(self, data):
        """ Transform the given data to the given kind.

            :param     data: the data to be transform
            :param str kind: the kind of data of the transformed data

            :return: the data of the given kind
        """
        logger = get_logger('transformer', logging.ERROR)
        logger.debug('Casting {}...'.format(data))

        if type(data) is not DataDefinition:
            logger.debug('Return right away.')
            return data

        if not data.transformation_required:
            logger.debug('Return without transformation.')
            return data.definition

        actual_data = data.definition
        actual_kind = data.kind

        returnee = self._cast(actual_data, actual_kind)

        logger.debug('Returning {}({})'.format(type(returnee).__name__, returnee))

        return returnee

    def _cast(self, actual_data, actual_kind):
        if actual_kind == 'entity':
            return self.__core_getter(actual_data)

        if actual_kind == 'class':
            return Loader(actual_data).package

        if actual_kind == 'int':
            return int(actual_data)

        if actual_kind == 'float':
            return float(actual_data)

        if actual_kind == 'bool':
            actual_data = actual_data.capitalize()

            assert actual_data in ('True', 'False')

            return actual_data == 'True'

        if actual_kind in ['list', 'tuple', 'set']:
            collection = []

            # At theis point, assume that actual_data is ParameterCollection.

            for item in actual_data.sequence():
                collection.append(self.cast(item))

            if actual_kind != 'list':
                collection = eval(actual_kind)(collection)

            return collection

        if actual_kind == 'dict':
            kv_map = {}

            # At theis point, assume that actual_data is ParameterCollection.

            for key, value in actual_data.items():
                kv_map[key] = self.cast(value)

            return kv_map

        if actual_kind == 'str':
            return str(actual_data)

        error_message = 'Unknown type: {} (Given data type: {})'
        raise ValueError(error_message.format(actual_kind,
                                              type(actual_data).__name__))
