# v2
from ..core  import Imagination
from ..debug import dump_meta_container, get_logger

from .xml import XMLParser

log = get_logger(__name__)


class UnsupportedConfigFileError(RuntimeError):
    """ Error when detect unsupported configuration file """


class Assembler(object):
    def __init__(self, core : Imagination = None):
        self._parsers = [
            XMLParser(),
        ]

        if core and core.in_standalone_mode():
            log.info(f'The container in the standalone mode has been provided.')

        self._core = core or Imagination()

    @property
    def core(self):
        return self._core

    def load(self, *filepaths):
        meta_container_map = self._load_config_files(*filepaths)

        self.core.update_metadata(meta_container_map)

    def _load_config_files(self, *filepaths):
        meta_container_map = {}

        for filepath in filepaths:
            config_handled = False

            for parser in self._parsers:
                if not parser.can_handle(filepath):
                    continue

                sub_meta_container_map = parser.parse(filepath)

                meta_container_map.update(sub_meta_container_map)

                config_handled = True

            if not config_handled:
                raise UnsupportedConfigFileError(filepath)

        return meta_container_map
