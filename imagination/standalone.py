"""
Imagination - Standalone Container
##################################

This is made to allow developers to quickly use the Imagination container with
any programming frameworks.

.. note::

    The setup of the container in the standalone module is made to as simple as
    possible whil the functionality should be the same as anyone manually sets
    up the container.

"""
import logging
import os

from .assembler.core import Assembler
from .debug          import get_logger

def initialize_from(config_filepath):
    logger = get_logger('standalone_container')

    lookup_paths = [
        os.path.join(os.getcwd(), 'imagination.xml'),
        os.path.join(os.getcwd(), 'services.xml'),
    ]

    if config_filepath:
        logger.debug('[initialize_from] Non-default configuration file path has been defined.')
        lookup_paths.insert(0, config_filepath)

    loading_targets = []

    for lookup_path in lookup_paths:
        if not os.path.exists(lookup_path):

            if config_filepath == lookup_path:
                logger.warning('[initialize_from] {} was given but does not exist.'.format(os.path.abspath(lookup_path)))

            continue

        logger.debug('[initialize_from] Loading configuration from {}...'.format(os.path.abspath(lookup_path)))
        loading_targets.append(lookup_path)

    assembler = Assembler()
    assembler.load(*loading_targets)

    return assembler.core

container = initialize_from(os.getenv('IMAGINATION_CONF_FILEPATH'))
