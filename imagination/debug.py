# v2
import logging
import os
import pprint
import sys
import typing

import imagination

_working_dir        = os.getcwd()
_module_path        = imagination.__path__[0]
_run_locally        = _module_path[:len(_working_dir)] == _working_dir
_in_testing         = 'unittest' in sys.modules
_in_testing_debug   = _in_testing and '-v' in sys.argv



def get_logger(namespace, level = None):
    return LoggerFactory.get(namespace, level)


class LoggerFactory:
    __known_logger__ = dict()

    @staticmethod
    def get(name: str, level: typing.Optional[int] = None):
        if name in LoggerFactory.__known_logger__:
            return LoggerFactory.__known_logger__.get(name)

        level = level or getattr(logging, (os.getenv('IMAGINATION_LOG_LEVEL') or 'WARNING').upper())
        minimalistic_mode = not (os.getenv('IMAGINATION_VERBOSE_LOG') in ('1', 'true'))

        formatter = logging.Formatter(
            '%(name)s: %(message)s'
            if minimalistic_mode
            else '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(level)

        logger = logging.Logger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        LoggerFactory.__known_logger__[name] = logger

        return logger


class PrintableMixin(object):
    def __repr__(self):
        classinfo = type(self)
        props     = dir(self)
        exported  = []
        fqcn      = classinfo.__name__

        if classinfo.__module__:
            fqcn = '{}.{}'.format(classinfo.__module__, fqcn)

        for prop_name in props:
            if prop_name[0] == '_':
                continue

            prop = getattr(self, prop_name)

            if callable(prop):
                continue

            exported.append('{}="{}"'.format(prop_name, prop))

        if not exported:
            return '<{}>'.format(fqcn)

        return '<{} {}>'.format(fqcn, ' '.join(exported))


def dump_meta_container(metadata):
    params = metadata.params

    data = {
        'id'           : metadata.id,
        'class'        : metadata.fqcn,
        'dependencies' : metadata.dependencies,
        'params'       : {
            'sequence' : [i for i in params.sequence()],
            'items'    : {k: v for k, v in params.items()},
        },
    }

    pprint.pprint(data,
                  indent = 2,
                  stream = sys.stderr if _in_testing_debug else sys.stdout)
