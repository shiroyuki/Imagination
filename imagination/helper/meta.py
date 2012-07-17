'''
:Author: Juti Noppornpitak

The module contains the data structures to aid the analysis and construction of
the loaders and entities based on the configuration.

.. note::
    Copyright (c) 2012 Juti Noppornpitak

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

from kotoba.kotoba import Kotoba

from imagination.decorator.validator import restrict_type
from imagination.exception import *
from imagination.loader import Loader
from imagination.locator import Locator

class Transformer(object):
    '''
    Data transformer

    :param `locator`: the entity locator (as an instance of :class:`imagination.locator.Locator`)
    '''
    @restrict_type(Locator)
    def __init__(self, locator):
        assert isinstance(locator, Locator), "Expecting an instance of imagination.locator.Locator, one of %s was given instead." % (type(locator).__name__)

        self.__locator = locator

    def cast(self, data, kind):
        '''
        Transform the given data to the given kind.

        :param `data`: the data to be transform
        :param `kind`: the kind of data of the transformed data
        :returns: the data of the given kind
        '''

        if kind == 'entity':
            data = self.__locator.get(data)
        elif kind == 'class':
            data = Loader(data).package()
        elif kind == 'int':
            data = int(data)
        elif kind == 'float':
            data = float(data)
        elif kind == 'bool':
            data = unicode(data).capitalize()

            assert data == 'True' or data == 'False'

            data = data == 'True'

        return data

    def locator(self):
        return self.__locator

class Interception(object):
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

    :param `largs`:  a list of arguments
    :param `kwargs`: a dictionary of arguments
    '''
    def __init__(self, largs=None, kwargs=None):
        self.largs  = largs  or []
        self.kwargs = kwargs or {}
