'''
:Author: Juti Noppornpitak
:Availability: 1.9

The module contains the package entity used to be an intermediate between :class:`imagination.locator.Locator`
and :class:`imagination.loader.Loader` and simulate the singleton class on the package in the Loader.

.. note::
    Copyright (c) 2015 Juti Noppornpitak

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
from imagination.common              import InterceptableObject
from imagination.proxy               import Proxy

class NonCallableFactoryMethod(RuntimeError):
    """ The factory method is not callable. """

class NotReadyError(RuntimeError):
    """ When the factory service is not ready to use. """

class Factorization(InterceptableObject):
    """
    Factorization Entity

    :param imagination.locator.Locator locator:    the locator
    :param str factory_id:     the factory entity identifier
    :param str factory_method: the factory method

    .. versionadded:: 1.9
    """
    def __init__(self, locator, factory_id, factory_method, parameters):
        super(Factorization, self).__init__()

        self._locator        = locator
        self._factory_id     = factory_id
        self._factory_method = factory_method
        self._parameters     = parameters
        self._reference      = None
        self._tags     = []

    @property
    def id(self):
        ''' Get the identifier of the proxy. '''
        return self.__id

    @property
    def tags(self):
        '''
        Retrieve the entity tags.

        :rtype: list
        '''
        return self._tags

    @tags.setter
    @restrict_type(list)
    def tags(self, tags):
        '''
        Define the entire entity tags.

        :param tags: new tags as replacements
        :type  tags: list or tuple
        '''
        if self.locked:
            raise LockedEntityException

        self._tags = tags

    def fork(self):
        ''' Fork the entity. '''
        self._prepare()

        factory = self._locator.get(self._factory_id)

        if isinstance(factory, Proxy):
            raise NotReadyError(self._factory_id)

        factory_method = factory.__getattribute__(self._factory_method)

        if not factory_method or not callable(factory_method):
            raise NonCallableFactoryMethod('{}.{} not available ({})'.format(self._factory_id, self._factory_method, type(factory_method)))

        self._reference = factory_method(*self._parameters.largs, **self._parameters.kwargs)

        if self._interceptable and isinstance(self._reference, object):
            self._bind_interceptions(self._reference, self._interceptions)

        return self._reference

    def _prepare(self):
        p = self._parameters

        for i in range(len(p.largs)):
            if isinstance(p.largs[i], Proxy):
                p.largs[i] = p.largs[i].load()

        for i in p.kwargs:
            if isinstance(p.kwargs[i], Proxy):
                p.kwargs[i] = p.kwargs[i].load()
