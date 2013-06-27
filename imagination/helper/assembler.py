'''
.. versionadded:: 1.5

Copyright (c) 2012-2013 Juti Noppornpitak

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

from re import split

from kotoba.kotoba import Kotoba
from kotoba        import load_from_file

from imagination.decorator.validator import restrict_type
from imagination.entity              import Entity
from imagination.exception           import *
from imagination.loader              import Loader
from imagination.helper.data         import *
from imagination.meta.aspect         import Contact
from imagination.meta.interception   import Interception
from imagination.meta.package        import Parameter
from imagination.proxy               import Proxy

class Assembler(object):
    '''
    The entity assembler via configuration files.

    :param `transformer`: an instance of :class:`imagination.helper.data.Transformer`

    '''

    __known_interceptable_events = ['before', 'pre', 'post', 'after']

    @restrict_type(Transformer)
    def __init__(self, transformer):
        self.__interceptions = []
        self.__transformer   = transformer
        self.__known_proxies = {}

    def activate_passive_loading(self):
        self.locator.in_passive_mode = True

    def deactivate_passive_loading(self):
        self.locator.in_passive_mode = False

    def load(self, filepath):
        '''
        Load the configuration.

        :param filepath: the file path to the configuration.
        :type  filepath: string or unicode
        '''
        xml = load_from_file(filepath)

        # First, register proxies to entities (for lazy initialization).
        for node in xml.children():
            self.__validate_node(node)
            self.__register_proxy(node)

        # Then, register loaders for entities.
        for node in xml.children():
            self.__get_interceptions(node)
            self.__register_loader(node)

        # Then, declare interceptions to target entities.
        for interception in self.__interceptions:
            self.locator\
                .get_wrapper(interception.actor.id)\
                .register_interception(interception)

        self.__interceptions = []

    @property
    def locator(self):
        '''
        The injected locator via the data transformer.

        :rtype: imagination.locator.Locator
        '''
        return self.__transformer.locator()

    @restrict_type(Kotoba)
    def __validate_node(self, node):
        if not node.attribute('id'):
            raise IncompatibleBlockError('Invalid entity configuration. No ID specified.')

        if not node.attribute('class'):
            raise IncompatibleBlockError('Invalid entity configuration. No class type specified.')

    @restrict_type(Kotoba)
    def __register_proxy(self, node):
        id    = node.attribute('id')
        proxy = Proxy(self.locator, id)

        self.locator.set(id, proxy)

        # this is for interceptors
        self.__known_proxies[id] = proxy

    @restrict_type(Kotoba)
    def __register_loader(self, node):
        id     = node.attribute('id')
        kind   = node.attribute('class')
        params = self.__get_params(node)
        tags   = self.__get_tags(node)

        loader = Loader(kind)

        entity = Entity(id, loader, *params.largs, **params.kwargs)

        entity.interceptable = self.__transformer.cast(node.attribute('interceptable') or 'true', 'bool')
        entity.tags          = tags

        self.locator.set(id, entity)

    @restrict_type(Kotoba)
    def __get_tags(self, node):
        tags = node.attribute('tags')

        return tags and split(' ', tags.strip()) or []

    @restrict_type(Kotoba)
    def __get_interceptions(self, node):
        for sub_node in node.children('interception'):
            self.__interceptions.append(self.__get_interception(sub_node))

    @restrict_type(Kotoba)
    def __get_interception(self, node):
        actor = None
        event = None

        intercepted_action = None
        handling_action    = None

        for given_event in self.__known_interceptable_events:
            given_actor = node.attribute(given_event)

            # If the actor is not defined, continue or if the event is already
            # set (in the earlier iteration), raise the exception.
            if not given_actor:
                continue
            elif event:
                raise MultipleInterceptingEventsWarning(given_event)

            # Initially get the name of the actor and the handler.
            actor   = given_actor
            handler = node.parent().attribute('id')

            if actor == Interception.self_reference_keyword():
                actor = handler

            # If the actor or the handler has no proxies, raise the exception.
            if actor not in self.__known_proxies:
                raise UnknownProxyError('The target (%s) of the interception is unknown.' % actor)

            if handler not in self.__known_proxies:
                raise UnknownProxyError('The handler (%s) of the interception is unknown.' % handler)

            actor   = Contact(self.__known_proxies[actor], node.attribute('do'))
            handler = Contact(self.__known_proxies[handler], node.attribute('with'), self.__get_params(node))
            event   = given_event

        return Interception(event, actor, handler)

    @restrict_type(Kotoba)
    def __get_params(self, node):
        package = Parameter()

        index = 0

        for param in node.children('param'):
            try:
                assert param.attribute('name')\
                    or param.attribute('type'),\
                    'The parameter #%d does not have either name or type.' % index
            except AssertionError as e:
                raise IncompatibleBlockError(e.message)

            index += 1
            name   = param.attribute('name')

            if name in package.kwargs:
                raise DuplicateKeyWarning('There is a parameter name "%s" with that name already registered.' % name)
                pass

            package.kwargs[name] = self.__transformer.cast(
                param,
                param.attribute('type')
            )

        return package
