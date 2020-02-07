"""
Imagination - Standalone Container
##################################

This is made to allow developers to quickly use the Imagination container with
any programming frameworks.

.. note::

    The setup of the container in the standalone module is made to as simple as
    possible while the functionality should be the same as anyone manually sets
    up the container.

"""
from importlib import import_module
import os

from .core           import Imagination
from .assembler.core import Assembler
from .debug          import get_logger

logger = get_logger(__name__)


def initialize_from(config_filepath) -> Imagination:
    lookup_paths = [
        os.path.join(os.getcwd(), 'imagination.xml'),
        os.path.join(os.getcwd(), 'services.xml'),
    ]

    if config_filepath:
        logger.debug('Non-default configuration file path has been defined.')
        lookup_paths.insert(0, config_filepath)

    loading_targets = []

    for lookup_path in lookup_paths:
        if not os.path.exists(lookup_path):

            if config_filepath == lookup_path:
                logger.warning('{} was given but does not exist.'.format(os.path.abspath(lookup_path)))

            continue

        logger.debug('Loading configuration from {}...'.format(os.path.abspath(lookup_path)))
        loading_targets.append(lookup_path)

    core = Imagination(standalone_mode=True)
    assembler = Assembler(core)

    if loading_targets:
        assembler.load(*loading_targets)
    else:
        logger.info('No configuration file has been loaded')

    return assembler.core


def load_config_file(config_filepath: str):
    global container

    updated_assembler = Assembler(container)
    updated_assembler.load(config_filepath)


def scan_recursively(code_path:str):
    # working with annotation
    m = import_module(code_path)

    module_file_path = m.__file__
    path_to_walk = os.path.dirname(module_file_path)

    if os.path.basename(module_file_path) != '__init__.py':
        return

    for sub_path in os.listdir(path_to_walk):
        if sub_path.startswith('_'):
            continue

        if not sub_path.endswith('.py'):
            continue

        next_code_path = '{}.{}'.format(code_path, sub_path[:-3])
        scan_recursively(next_code_path)


container = initialize_from(os.getenv('IMAGINATION_CONF_FILEPATH'))
