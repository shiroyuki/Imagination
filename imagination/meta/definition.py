# v2
from ..debug import PrintableMixin


class DuplicateParameterDefinitionWarning(Warning):
    """ Warning for Duplicate Parameter Definition """


class DataDefinition(PrintableMixin):
    """ Parameter/Data Definition

        :param definition: the definition, actual data, or value
        :param str name: the name of the parameter / data (optional means positional)
        :param str kind: the data type
        :param bool transformation_required: flag if data transformation required
    """
    def __init__(self, definition, name : str = None, kind : str = None,
                 transformation_required : bool = True):
        self.__name       = name
        self.__kind       = kind or 'str'
        self.__definition = definition

        self.__transformation_required = transformation_required

    @property
    def name(self):
        return self.__name

    @property
    def kind(self):
        return self.__kind

    @property
    def definition(self):
        return self.__definition

    @property
    def transformation_required(self):
        return self.__transformation_required


class ParameterCollection(PrintableMixin):
    def __init__(self):
        self.__list = list()
        self.__map  = dict()

    @property
    def all(self):
        return {
            'sequence': [i for i in self.sequence()],
            'items': {k: v for k, v in self.items()},
        }

    def sequence(self):
        for item in self.__list:
            yield item

    def items(self):
        for k, v in self.__map.items():
            yield k, v

    def add(self, meta_parameter : DataDefinition, name = None):
        if not name:
            self.__list.append(meta_parameter)

            return

        if name in self.__map:
            raise DuplicateParameterDefinitionWarning(name)

        self.__map[name] = meta_parameter

    def __len__(self):
        return len(self.__list) + len(self.__map)


class Interception(PrintableMixin):
    """ Metadata for Interception

        .. note::

            The "before" event is now the same as "pre" and "after" is the same
            as "post" from version 2. The "pre" and "post" events will be
            deprecated.
    """
    __self_references__ = {'self', 'me'}  # "me" is a legacy self-reference.
    __known_events__    = ('before', 'after', 'error', 'pre', 'post')
    __remap_events__    = {'pre': 'before', 'post': 'after'}

    def __init__(self,
                 when_to_intercept   : str,
                 intercepted_id      : str,
                 method_to_intercept : str,
                 interceptor_id      : str,
                 intercepting_method : str
                 ):

        assert when_to_intercept in self.__known_events__, 'Unknown event given ({})'.format(when_to_intercept)
        assert method_to_intercept and interceptor_id and intercepting_method

        # NOTE Remap for PARTIAL backward compatibility.
        if when_to_intercept in self.__remap_events__:
            when_to_intercept = self.__remap_events__[when_to_intercept]

        self._when_to_intercept   = when_to_intercept
        self._intercepted_id      = intercepted_id
        self._method_to_intercept = method_to_intercept
        self._interceptor_id      = interceptor_id
        self._intercepting_method = intercepting_method

    @property
    def when_to_intercept(self):
        return self._when_to_intercept

    @property
    def intercepted_id(self):
        return self._intercepted_id

    @property
    def method_to_intercept(self):
        return self._method_to_intercept

    @property
    def interceptor_id(self):
        return self._interceptor_id

    @property
    def intercepting_method(self):
        return self._intercepting_method

    def is_self_interception(self):
        return self._interceptor_id in self.__self_references__


class MethodCall(object):
    def __init__(self, actor_id, method_name, parameters):
        self.actor_id    = actor_id
        self.method_name = method_name
        self.parameters  = parameters


class SubDependency(object):
    def __init__(self, service_id):
        self.service_id  = service_id