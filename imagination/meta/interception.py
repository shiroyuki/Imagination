'''
:Author: Juti Noppornpitak
:Availability: 1.5

The module contains the data structure of method interception to aid the analysis
and construction of the loaders and entities based on the configuration.

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

from imagination.decorator.validator import restrict_type, SpecialType
from imagination.meta.package        import Parameter
from imagination.proxy               import Proxy

class Interception(object):
    '''
    .. note::
        Please note that both `Interception.actor` and `Interception.handler`
        are always instances of :class:`imagination.proxy.Proxy`. This is
        intentional in order to avoid direct circular dependencies.
    '''

    @restrict_type(unicode, Proxy, unicode, Proxy, unicode, Parameter)
    def __init__(self, event, actor, intercepted_action, handler, handling_action, handling_parameters):
        self.actor   = actor
        self.event   = event
        self.handler = handler

        self.intercepted_action  = intercepted_action
        self.handling_action     = handling_action
        self.handling_parameters = handling_parameters

    @staticmethod
    def self_reference_keyword():
        return 'me'

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