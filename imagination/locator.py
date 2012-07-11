'''
:Author: Juti Noppornpitak

The module contains the entity locator used to promote reusability of components.

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

from re     import split
from kotoba import load_from_file

from imagination.entity    import Entity, Proxy
from imagination.exception import IncompatibleBlockError, UnknownEntityError, UnknownFileError
from imagination.loader    import Loader

class Locator(object):
    ''' Entity locator '''

    def __init__(self):
        self._entities = {}
        self._tag_to_entity_ids = {}

    def fork(self, id):
        '''
        Fork the entity identified by ``id``.

        :param `id`: entity identifier
        '''
        try:
            return self._entities[id].fork()
        except KeyError:
            raise UnknownEntityError, 'The requested entity named "%s" is unknown or not found.' % id

    def get(self, id):
        '''
        Retrieve the entity identified by ``id``.

        :param `id`: entity identifier
        :returns: the requested entity
        '''
        try:
            entity = self._entities[id]

            return isinstance(entity, Entity) and entity.instance() or entity
        except KeyError:
            raise UnknownEntityError, 'The requested entity named "%s" is unknown or not found.' % id

    def get_list_by_tag(self, tag_label):
        '''
        Retrieve entities by *tag_label*.

        :param `tag_label`: tag label
        '''

        # First, get the entity identifiers.
        if tag_label not in self._tag_to_entity_ids:
            return []

        # Then, get references to entities.
        return [self.get(entity_id) for entity_id in self._tag_to_entity_ids[tag_label]]

    def set(self, id, entity):
        ''' Set the given *entity* by *id*. '''

        if not isinstance(entity, Entity) and not isinstance(entity, Proxy):
            raise UnknownEntityError, 'The type of the given entity named "%s" is not excepted.' % id

        if isinstance(entity, Entity):
            entity.lock()

        self._entities[id] = entity

        if isinstance(entity, Proxy):
            return

        for tag in entity.tags():
            if not self._tag_to_entity_ids.has_key(tag):
                self._tag_to_entity_ids[tag] = []

            self._tag_to_entity_ids[tag].append(entity.id())

    def has(self, id):
        ''' Check if the entity with *id* is already registered. '''
        return id in self._entities

    def load_xml(self, file_path):
        '''
        Load the entities from a XML configuration file at *file_path*.

        .. code-block:: xml

            <?xml version="1.0" encoding="utf-8"?>
            <!-- This example simulates how to set up a service with Imagination. -->
            <imagination>
                <entity id="finder" class="tori.common.Finder"></entity>

                <!-- Example of injecting a class reference. -->
                <entity id="db" class="tori.service.rdb.EntityService">
                    <param name="url">sqlite:///:memory:</param>
                    <param name="entity_type" type="class">core.model.Log</param>
                </entity>

                <!-- Example of injecting a service. -->
                <entity id="markdown-doc" class="app.note.service.MDDocumentService">
                    <param name="finder" type="id">finder</param>
                    <param name="location">/Users/jnopporn/Documents</param>
                </entity>
            </imagination>

        The parameter of type ``class`` is only representing the reference of the class.

        :Status: Deprecated in 1.5

        '''
        xml = load_from_file(file_path)

        # First, register entities as proxies (for lazy initialization).
        for block in xml.children():
            self._validate_block(block)

            entity_id = block.attribute('id')
            proxy     = Proxy(self, entity_id)

            self.set(entity_id, proxy)

        # Then, register entities with loaders.
        for block in xml.children():
            entity_id    = block.attribute('id')
            reference    = block.attribute('class')
            args, kwargs = self._retrieve_params(block)
            loader       = Loader(reference)

            tags = block.attribute('tags')
            if tags:
                tags = tags.strip()
                tags = tags and split(' ', tags) or []

            entity = Entity(entity_id, loader, **kwargs)
            entity.tags(tags)

            self.set(entity_id, entity)

    def transform_data(self, data, kind):
        '''
        Transform the given data to the given kind.

        :param `data`: the data to be transform
        :param `kind`: the kind of data of the transformed data.
        :returns: the data of the given kind.
        '''

        if kind == 'entity':
            data = self.get(data)
        elif kind == 'class':
            data = Loader(data).package()
        elif kind == 'int':
            data = int(data)
        elif kind == 'float':
            data = float(data)
        elif kind == 'bool':
            data = unicode(data).capitalize() == 'True'

        return data

    def _validate_block(self, block):
        if not block.attribute('id'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No ID specified.'

        if not block.attribute('class'):
            raise IncompatibleBlockError, 'Invalid entity configuration. No class type specified.'

    def _retrieve_params(self, block):
        args   = []
        kwargs = {}

        for param in block.children('param'):
            kwargs.update(self.transform_param(param))

        return args, kwargs

    def transform_param(self, param):
        if not param.attribute('name'):
            raise IncompatibleBlockError, 'What is the name of the parameter?'

        return {
            param.attribute('name'): self.transform_data(
                param.data(),
                param.attribute('type')
            )
        }
