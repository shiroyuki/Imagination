'''
:Author: Juti Noppornpitak

The module contains the entity locator used to promote reusability of components.
'''

from yotsuba.lib.kotoba    import Kotoba
from imagination.entity    import Entity
from imagination.exception import IncompatibleBlockError, UnknownEntityError, UnknownFileError
from imagination.loader    import Loader

class Locator(object):
    ''' Entity locator '''
    
    def __init__(self):
        self._entities = {}
    
    def get(self, id):
        ''' Get the entity by *id*. '''
        try:
            return self._entities[id].instance()
        except KeyError:
            raise UnknownEntityError, 'The requested entity named "%s" is unknown or not found.' % id
    
    def set(self, id, entity):
        ''' Set the given *entity* by *id*. '''
        
        if not isinstance(entity, Entity):
            raise UnknownEntityError, 'The type of the given entity named "%s" is not excepted.' % id
        
        self._entities[id] = entity
    
    def has(self, id):
        ''' Check if the entity with *id* is already registered. '''
        return id in self._entities
    
    def load_xml(self, file_path):
        '''
        Load the entities from a XML configuration file at *file_path*.
        
        .. code-block:: xml
        
            <?xml version="1.0" encoding="utf-8"?>
            <!-- This example simulates how to set up a service with Imagination. -->
            <locator>
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
            </locator>
        
        The parameter of type ``class`` is only representing the reference of the class.
        
        '''
        xml      = Kotoba(file_path)
        selector = 'imagination > entity'
        
        # Register additional services first.
        for block in xml.get(selector):
            self._validate_block(block)
            
            entity_id = block.attrs['id']
            
            reference = block.attrs['class']
            kwargs    = self._retrieve_params_from_block(block)
            
            loader    = Loader(reference)
            entity    = Entity(entity_id, loader, **kwargs)
            
            self.set(entity_id, entity)
    
    def _dict_get_key(self, dictionary, key):
        return dictionary.attrs.has_key(key) and dictionary.attrs[key]
    
    def _validate_block(self, block):
        if not self._dict_get_key(block, 'id'):
            raise IncompatibleBlockError, 'What is the identifier of the entity?'
            
        if not self._dict_get_key(block, 'class'):
            raise IncompatibleBlockError, 'What is the name of the class of the entity?'
    
    def _retrieve_params_from_block(self, block):
        kwargs = {}
            
        for param in block.get('param'):
            param_name, param_data = self._analyze_param(param)
            kwargs[param_name]     = param_data
        
        return kwargs
    
    def _analyze_param(self, param):
        if not self._dict_get_key(param, 'name'):
            raise IncompatibleBlockError, 'What is the name of the parameter?'
                
        param_name = param.attrs['name']
        param_data = param.data()
        param_type = self._dict_get_key(param, 'type') or None
        
        # Automatically convert data type.
        if param_type == 'entity':
            param_data = self.get(param_data)
        elif param_type == 'class':
            param_data = Loader(param_data).package()
        elif param_type == 'int':
            param_data = int(param_data)
        elif param_type == 'float':
            param_data = float(param_data)
        elif param_type == 'bool':
            param_data = unicode(param_data).capitalize() == 'True'
        
        return (param_name, param_data)
