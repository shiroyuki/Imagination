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
from kotoba        import load_from_file

from imagination.decorator.validator import allowed_type
from imagination.entity      import Entity, Proxy
from imagination.exception   import IncompatibleBlockError, UnknownEntityError, UnknownFileError
from imagination.loader      import Loader
from imagination.helper.meta import Transformer

class Assembler(object):
    '''
    :param `transformer`: an instance of :class:`imagination.helper.meta.Transformer`
    '''
    def __init__(self, transformer):
        try:
            assert isinstance(transformer, Transformer)
        except AssertionError, e:
            raise TypeError, 'Expected an instance of %s, given %s.'\
                % (Transformer, transformer.__class__)

        self.__transformer = transformer
        self.__locator   = None

    def load(self, filepath):
        xml = load_from_file(filepath)

        # First, register proxies to entities (for lazy initialization).
        for node in xml.children():
            self.__register_proxy(node)

        # Then, register loaders for entities.
        for node in xml.children():
            self.__register_loader(node)

    def locator(self):
        if not self.__locator:
            self.__locator = self.__transformer.locator()

        return self.__locator

    def __validate_node(self, node):
        if not node.attribute('id'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No ID specified.'

        if not node.attribute('class'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No class type specified.'

    @allowed_type(Kotoba)
    def __register_proxy(self, node):
        self.__validate_node(node)

        id      = node.attribute('id')
        proxy   = Proxy(self.locator(), id)

        self.locator().set(id, proxy)

    @allowed_type(Kotoba)
    def __register_loader(self, node):
        id     = node.attribute('id')
        kind   = node.attribute('class')
        params = self.__get_params(node)
        tags   = self.__get_tags(node)
        loader = Loader(kind)
        entity = Entity(id, loader, **kwargs)

        entity.tags(tags)

        self.locator().set(id, entity)

    @allowed_type(Kotoba)
    def __get_tags(self, node):
        tags = node.attribute('tags').strip()

        return tags and split(' ', tags) or []

    @allowed_type(Kotoba)
    def __get_params(self, node):
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

            package.kwargs[name] = self.__transformer.cast(
                param.data(),
                param.attribute('type')
            )

        return package