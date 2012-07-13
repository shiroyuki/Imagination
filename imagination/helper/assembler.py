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

from imagination.decorator.validator import restrict_type
from imagination.entity      import Entity, Proxy
from imagination.exception   import IncompatibleBlockError, UnknownEntityError, UnknownFileError
from imagination.loader      import Loader
from imagination.helper.meta import *

class Assembler(object):
    '''
    :param `transformer`: an instance of :class:`imagination.helper.meta.Transformer`
    '''

    __known_interceptable_events = ['before', 'pre', 'post', 'after']

    @restrict_type(Transformer)
    def __init__(self, transformer):
        self.__transformer = transformer

    @restrict_type(unicode)
    def load(self, filepath):
        xml = load_from_file(filepath)

        # First, register proxies to entities (for lazy initialization).
        for node in xml.children():
            self.__register_proxy(node)

        # Then, register loaders for entities.
        for node in xml.children():
            self.__register_loader(node)

    def locator(self):
        return self.__transformer.locator()

    @restrict_type(Kotoba)
    def __validate_node(self, node):
        if not node.attribute('id'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No ID specified.'

        if not node.attribute('class'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No class type specified.'

    @restrict_type(Kotoba)
    def __register_proxy(self, node):
        self.__validate_node(node)

        id    = node.attribute('id')
        proxy = Proxy(self.locator(), id)

        self.locator().set(id, proxy)

    @restrict_type(Kotoba)
    def __register_loader(self, node):
        interceptions = self.__get_interceptions(node)

        id     = node.attribute('id')
        kind   = node.attribute('class')
        params = self.__get_params(node)
        tags   = self.__get_tags(node)

        loader = Loader(kind)

        entity = Entity(id, loader, *params.largs, **params.kwargs)
        entity.tags(tags)

        self.locator().set(id, entity)

    @restrict_type(Kotoba)
    def __get_tags(self, node):
        tags = node.attribute('tags')

        return tags and split(' ', tags.strip()) or []

    @restrict_type(Kotoba)
    def __get_interceptions(self, node):
        interceptions = []

        for sub_node in node.children('interception'):
            interceptions.append(self.__get_interception(sub_node))

        return interceptions

    @restrict_type(Kotoba)
    def __get_interception(self, node):
        actor = None
        event = None

        intercepted_action = None
        handling_action    = None

        for given_event in self.__known_interceptable_events:
            given_actor = node.attribute(given_event)

            if given_actor and not event:
                actor = given_actor
                event = given_event
            elif given_actor and event:
                raise MultipleInterceptingEventsWarning, given_event

            intercepted_action = node.attribute('do')
            handling_action    = node.attribute('with')

        return Interception(
            event,
            actor,
            intercepted_action,
            node.parent().attribute('id'),
            handling_action
        )

    @restrict_type(Kotoba)
    def __get_params(self, node):
        package = ParameterPackage()

        index = 0

        for param in node.children('param'):
            try:
                assert param.attribute('name')\
                    or param.attribute('type'),\
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
