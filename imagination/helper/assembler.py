'''
:Author: Juti Noppornpitak

The module contains the assembler to constuct loaders and entites based on the configuration
and register to a particular locator.

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

from imagination.decorator.validator import allowed_type
from imagination.helper.meta import *

class Assembler(object):
    '''
    :param `transformer`: an instance of :class:`imagination.helper.meta.Transformer`
    '''
    def __init__(self, transformer):
        try:
            assert isinstance(transformer, Transformer), 'imagination.helper.meta.Transformer'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message

        self.transformer = transformer

    @allowed_type(Kotoba)
    def get_entity(self, node):
        '''
        :param `node`: an instance of :class:`kotoba.kotoba.Kotoba`
        '''
        try:
            assert isinstance(node, Kotoba), 'kotoba.kotoba.Kotoba'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message


    def get_param(self, node):
        '''
        :param `node`: an instance of :class:`kotoba.kotoba.Kotoba`
        '''
        try:
            assert isinstance(node, Kotoba), 'kotoba.kotoba.Kotoba'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message

        package = ParameterPackage(node)

        index = 0

        for param in node.children('param'):
            try:
                assert not param.attribute('name')\
                    or not param.attribute('type'),\
                    'The parameter #%d does not have either name or type.' % index
            except AssertionError, e:
                raise IncompatibleBlockError, e.message

            index += 1
            name   = param.attribute('name')

            if package.kwargs.has_key(name):
                raise DuplicateKeyWarning, 'There is a paramenter with that name already registered.'

            package.kwargs[name] = transformer.cast(
                param.data(),
                param.attribute('type')
            )

        return package