from kotoba.kotoba import Kotoba

from imagination.decorator.validator import restrict_type
from imagination.exception import *
from imagination.loader import Loader
from imagination.locator import Locator

class Transformer(object):
    """
    Data transformer

    .. versionadded: 1.5

    :param imagination.locator.Locator locator: the entity locator
    """
    @restrict_type(Locator)
    def __init__(self, locator):
        assert locator and isinstance(locator, Locator), "Expecting an instance of imagination.locator.Locator, one of %s was given instead." % (type(locator).__name__)

        self.__locator = locator

    def cast(self, data, kind):
        '''
        Transform the given data to the given kind.

        :param data: the data to be transform
        :param str kind: the kind of data of the transformed data
        :return: the data of the given kind
        '''

        actual_data = data.data() if isinstance(data, Kotoba) else data

        if kind == 'entity':
            actual_data = self.__locator.get(actual_data)
        elif kind == 'class':
            actual_data = Loader(actual_data).package
        elif kind == 'int':
            actual_data = int(actual_data)
        elif kind == 'float':
            actual_data = float(actual_data)
        elif kind == 'bool':
            actual_data = actual_data.capitalize()

            assert actual_data == 'True' or actual_data == 'False'

            actual_data = actual_data == 'True'
        elif kind in ['list', 'tuple', 'set']:
            assert isinstance(data, Kotoba), 'Asking for a Kotoba object, getting an instance of type {}.'.format(type(data).__name__)

            actual_data = []

            for item in data.children():
                item_type = item.attribute('type')

                actual_data.append(self.cast(item, item_type))

            if kind != 'list':
                actual_data = eval(kind)(actual_data)
        elif kind == 'dict':
            assert isinstance(data, Kotoba), 'Asking for a Kotoba object, getting an instance of type {}.'.format(type(data).__name__)

            actual_data = {}

            for item in data.children():
                item_name = item.attribute('name')
                item_type = item.attribute('type')

                actual_data[item_name] = self.cast(item, item_type)
        elif kind == 'str':
            actual_data = str(actual_data)
        elif kind not in ['str', 'unicode']:
            raise ValueError('Unknown type: {} (Given data: {})'.format(kind, data))

        return actual_data

    def locator(self):
        return self.__locator

class Interception(object):
    """ Event Interception

        :param str event: the event type
        :param str actor: the ID of the actor
        :param str intercepted_action: the intercepted method
        :param str handler: the ID of the handler (interceptor)
        :param str handling_action: the handing (intercepting) method
    """
    __self_reference_keyword = 'me'

    def __init__(self, event, actor, intercepted_action, handler, handling_action):
        self.actor   = actor == self.__self_reference_keyword and handler or actor
        self.event   = event
        self.handler = handler

        self.intercepted_action = intercepted_action
        self.handling_action    = handling_action

    def __str__(self):
        return 'Interception: %s %s.%s, %s.%s' % (
            self.event,
            self.actor,
            self.intercepted_action,
            self.handler,
            self.handling_action
        )

    def __unicode__(self):
        return u'Interception: %s %s.%s, %s.%s' % (
            self.event,
            self.actor,
            self.intercepted_action,
            self.handler,
            self.handling_action
        )

class ParameterPackage(object):
    '''
    Parameter Package represents the parameter of arguments as
    a list and a dictionary to any callable objects (e.g.,
    constructor and methods).

    :param list largs:  a list of arguments
    :param dict kwargs: a dictionary of arguments
    '''
    def __init__(self, largs=None, kwargs=None):
        self.largs  = largs  or []
        self.kwargs = kwargs or {}
