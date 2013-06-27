'''
:Author: Juti Noppornpitak
:Availability: 1.5
:Usage: Internal

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

from imagination.decorator.validator import restrict_type
from imagination.meta.aspect         import Contact

class Interception(object):
    '''
    .. note::
        Please note that both `Interception.actor` and `Interception.handler`
        are always instances of :class:`imagination.proxy.Proxy`. This is
        intentional in order to avoid direct circular dependencies.
    '''

    static_guid = 1

    @restrict_type(str, Contact, Contact)
    def __init__(self, event, actor, handler):
        self._guid    = Interception.static_guid
        self._actor   = actor
        self._event   = event
        self._handler = handler

        Interception.static_guid += 1

    @property
    def actor(self):
        return self._actor

    @property
    def event(self):
        return self._event

    @property
    def handler(self):
        return self._handler

    @staticmethod
    def self_reference_keyword():
        return 'me'