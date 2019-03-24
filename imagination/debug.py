# v2
import logging
import os
import pprint
import sys

import imagination

_working_dir        = os.getcwd()
_module_path        = imagination.__path__[0]
_run_locally        = _module_path[:len(_working_dir)] == _working_dir
_in_testing         = 'unittest' in sys.modules
_in_testing_debug   = _in_testing and '-v' in sys.argv
_normal_logging_lv  = logging.INFO  if _run_locally      else logging.ERROR
_testing_logging_lv = logging.DEBUG if _in_testing_debug else logging.INFO
_default_logging_lv = _testing_logging_lv if _in_testing else _normal_logging_lv
_known_loggers      = {}
_env_log_level      = (getattr(logging, os.getenv('IMAGINATION_LOG_LEVEL'))
                       if os.getenv('IMAGINATION_LOG_LEVEL')
                       else None)


def get_logger(namespace, level = None, handler = None):
    global _run_locally, _in_testing_debug

    logger_name = '{}.{}'.format(imagination.__name__, namespace)

    if logger_name in _known_loggers:
        return _known_loggers[logger_name]

    logging_lv  = level or (_env_log_level or _default_logging_lv)
    logger      = logging.getLogger(logger_name)

    logger.setLevel(logging_lv)

    if _in_testing_debug:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging_lv)
    elif not handler:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging_lv)

    logger.addHandler(handler)

    _known_loggers[logger_name] = logger

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
