'''
:Author: Juti Noppornpitak
:Availability: 1.5

The module contains the package entity used to be an intermediate between :class:`imagination.locator.Locator`
and :class:`imagination.loader.Loader` and simulate the singleton class on the package in the Loader.

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

class Proxy(object):
    '''
    Proxy to a particular entity known by a certain locator.

    :param `locator`: the locator
    :param `id`: entity identifier
    '''
    def __init__(self, locator, id):
        self.__dict__ = {
            'id':      id,
            'locator': locator,
            'cache':   None,
        }

    def load(self):
        if not self.__dict__['cache']:
            self.__dict__['cache'] = self.__dict__['locator'].get(self.__dict__['id'])

        return self.__dict__['cache']

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        actual_object = self.load()

        if not hasattr(actual_object, name):
            raise AttributeError('{} has no attribute "{}".'.format(type(actual_object).__name__), name)

        return getattr(actual_object, name)
