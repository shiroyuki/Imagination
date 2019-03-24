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
import logging
from importlib import import_module
from inspect import ismodule
import os

from .core           import Imagination
from .assembler.core import Assembler
from .debug          import get_logger

logger = get_logger('standalone_container')


def initialize_from(config_filepath) -> Imagination:
    lookup_paths = [
        os.path.join(os.getcwd(), 'imagination.xml'),
        os.path.join(os.getcwd(), 'services.xml'),
    ]

    if config_filepath:
        logger.debug('[standalone.initialize_from] Non-default configuration file path has been defined.')
        lookup_paths.insert(0, config_filepath)

    loading_targets = []

    for lookup_path in lookup_paths:
        if not os.path.exists(lookup_path):

            if config_filepath == lookup_path:
                logger.warning('[standalone.initialize_from] {} was given but does not exist.'.format(os.path.abspath(lookup_path)))

            continue

        logger.debug('[standalone.initialize_from] Loading configuration from {}...'.format(os.path.abspath(lookup_path)))
        loading_targets.append(lookup_path)

    assembler = Assembler()

    if loading_targets:
        assembler.load(*loading_targets)
    else:
        logger.warning('[standalone.initialize_from] No configuration file has been loaded')

    return assembler.core


def load_config_file(config_filepath: str):
    global container

    updated_assembler = Assembler(container)
    updated_assembler.load(config_filepath)


def scan_recursively(code_path:str):
    # working with annotation
    logger.debug(f'Inspect: {code_path}')
    m = import_module(code_path)
    logger.debug(f'{m}')
    for p in dir(m):
        iterated_path = f'{code_path}.{p}'
        iterated_obj = getattr(m, p)

        if p[:2] == '__' and p[-2:] == '__':
            logger.debug(f'Ignored: {iterated_path}, {iterated_obj if isinstance(iterated_obj, str) else "[...]"}')

            continue

        logger.debug(f'Inspect: {iterated_path}, {type(iterated_obj).__name__}, {iterated_obj}')

    module_file_path = m.__file__
    path_to_walk = os.path.dirname(module_file_path)

    if os.path.basename(module_file_path) != '__init__.py':
        logger.debug(f'Stopped iterating after {module_file_path}')

        return

    for sub_path in os.listdir(path_to_walk):
        if sub_path.startswith('_'):
            continue

        if not sub_path.endswith('.py'):
            continue

        next_code_path = f'{code_path}.{sub_path[:-3]}'
        # print(next_code_path)
        scan_recursively(next_code_path)


container = initialize_from(os.getenv('IMAGINATION_CONF_FILEPATH'))
