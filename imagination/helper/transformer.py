# v2
import logging
import os
import re

from ..debug           import get_logger
from ..exc             import UnknownEnvironmentVariableError
from ..loader          import Loader
from ..meta.definition import DataDefinition


class Transformer(object):
    """ Data transformer """
    def __init__(self, core_getter : callable):
        self.__core_getter = core_getter

        self.__re_env_with_default_value_as_string = re.compile('\{\s*\$(?P<env_name>[A-Za-z0-9_\.]+) or "(?P<default>.+)"\s*\}', re.IGNORECASE)
        self.__re_env_with_default_value_as_int    = re.compile('\{\s*\$(?P<env_name>[A-Za-z0-9_\.]+) or (?P<default>[0-9]+)\s*\}', re.IGNORECASE)
        self.__re_env_with_default_value_as_float  = re.compile('\{\s*\$(?P<env_name>[A-Za-z0-9_\.]+) or (?P<default>[0-9]*\.[0-9]*)\s*\}', re.IGNORECASE)
        self.__re_env_without_default_value        = re.compile('\{\s*\$(?P<env_name>[A-Za-z0-9_\.]+)\s*\}', re.IGNORECASE)

    def cast(self, data, previously_activated : list = None):
        """ Transform the given data to the given kind.

            :param     data: the data to be transform
            :param str kind: the kind of data of the transformed data

            :return: the data of the given kind

            .. versionadded:: Imagination 2.5

                Added support for environment variables.

        """
        previously_activated = previously_activated or []

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

        returnee = self._cast(actual_data, actual_kind, previously_activated)

        logger.debug('Returning {}({})'.format(type(returnee).__name__, returnee))

        return returnee

    def _pre_process(self, data):
        if not isinstance(data, str):
            return data

        returnee = data

        check_sequence = [
            self.__re_env_without_default_value,
            self.__re_env_with_default_value_as_string,
            self.__re_env_with_default_value_as_float,
            self.__re_env_with_default_value_as_int,
        ]

        while True:
            matches      = None
            used_pattern = None

            for pattern in check_sequence:
                matches = pattern.search(returnee)

                if matches:
                    used_pattern = pattern

                    break

            if not matches:
                break

            parsed        = matches.groupdict()
            env_value     = os.getenv(parsed['env_name'])
            default_value = parsed['default'] if 'default' in parsed else ''

            if not env_value and not default_value:
                raise UnknownEnvironmentVariableError(parsed['env_name'])

            returnee = used_pattern.sub(env_value or default_value, returnee, count = 1)

        return returnee

    def _cast(self, actual_data, actual_kind, previously_activated):
        actual_data = self._pre_process(actual_data)

        if actual_kind == 'entity':
            return self.__core_getter(actual_data, previously_activated)

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
        raise ValueError(error_message.format(actual_kind, type(actual_data).__name__))
