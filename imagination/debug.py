# v2
import json
import logging
import os
import pprint
import re
import sys
import typing

import imagination

_working_dir        = os.getcwd()
_module_path        = imagination.__path__[0]
_run_locally        = _module_path[:len(_working_dir)] == _working_dir
_in_testing         = 'unittest' in sys.modules
_in_testing_debug   = _in_testing and '-v' in sys.argv


def get_logger(namespace,
               level: int = None,
               minimal: typing.Optional[bool] = None):
    return LoggerFactory.get(namespace,
                             level,
                             mode='compact' if minimal else 'full')


def get_logger_for(obj: object,
                   level: int = None,
                   minimal: typing.Optional[bool] = None):
    return LoggerFactory.get_for_object(obj,
                                        level,
                                        mode='compact' if minimal else 'full')


class JsonFormatter(logging.Formatter):
    def format(self, record) -> str:
        return json.dumps(dict(
            level=record.levelno,
            level_name=record.levelname,
            name=record.name,
            pathname=record.pathname,
            lineno=record.lineno,
            func=record.funcName,
            details=dict(
                msg=record.msg,
                args=record.args,
                exc_info=self.formatException(record.exc_info) if record.exc_info else None,
            ),
        ))


class LoggerFactory:
    __known_loggers__ = dict()

    @staticmethod
    def get_default_log_level() -> int:
        return getattr(logging, (os.getenv('IMAGINATION_LOG_LEVEL') or 'WARNING').upper())

    @staticmethod
    def get_logger_mode() -> str:
        """ Get the default logger mode

            Please note that the "json" mode always provides all information.

            Three modes are supported:
               * minimal - The timestamp will be excluded from the output.
               * compact - If the logger name is a fully qualified class name, the module names are truncated to ONE character per module.
               * full - If the logger name is a fully qualified class name, the whole FQCN will be used as the logger name.
               * json - Similar to "full", the output will be in JSON format.
        """
        return os.getenv('IMAGINATION_LOG_MODE') or 'compact'

    @classmethod
    def get(cls,
            name: str,
            level: typing.Optional[int] = None,
            handler: typing.Optional[logging.Handler] = None,
            formatter: typing.Optional[logging.Formatter] = None,
            mode: typing.Optional[str] = None,
            cache_key: typing.Optional[str] = None,
            ) -> logging.Logger:
        cache_key = cache_key or name

        if cache_key in cls.__known_loggers__:
            return cls.__known_loggers__.get(cache_key)

        level = level or cls.get_default_log_level()

        if not formatter:
            mode = mode or cls.get_logger_mode()

            if mode == 'json':
                formatter = JsonFormatter('%(message)s')
            else:
                if mode == 'minimal':
                    stdout_format = '%(levelname)s: %(name)s: %(message)s'
                else:
                    stdout_format = '[%(asctime)s] %(levelname)s: %(name)s: %(message)s'
                formatter = logging.Formatter(stdout_format)

        if not handler:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            handler.setLevel(level)

        logger = logging.Logger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        cls.__known_loggers__[cache_key] = logger

        return logger

    @classmethod
    def get_for_type(cls,
                     t: typing.Type,
                     level: typing.Optional[int] = None,
                     handler: typing.Optional[logging.Handler] = None,
                     formatter: typing.Optional[logging.Formatter] = None,
                     mode: typing.Optional[str] = None,
                     ):
        cache_key = f'{t.__module__}.{t.__name__}'
        mode = mode or cls.get_logger_mode()

        mod_name = t.__module__
        if mode in ['minimal', 'compact']:
            mod_name = '.'.join([
                (
                    ''.join([j[0] for j in re.split(r'_', i)])
                    if '_' in i
                    else i[0]
                )
                for i in re.split(r'\.', mod_name)
            ])

        logger_name = f'{mod_name}.{t.__name__}'
        return cls.get(name=logger_name,
                       level=level,
                       handler=handler,
                       formatter=formatter,
                       mode=mode,
                       cache_key=cache_key)

    @classmethod
    def get_for_object(cls,
                       obj: object,
                       level: typing.Optional[int] = None,
                       handler: typing.Optional[logging.Handler] = None,
                       formatter: typing.Optional[logging.Formatter] = None,
                       mode: typing.Optional[str] = None,
                       ):
        t = type(obj)
        return cls.get_for_type(t=t,
                                level=level,
                                handler=handler,
                                formatter=formatter,
                                mode=mode)

    @classmethod
    def instance(cls):
        if not hasattr(cls, '__instance__'):
            cls.__instance__ = cls()

        return cls.__instance__


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
