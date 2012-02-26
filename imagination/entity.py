'''
:Author: Juti Noppornpitak

The module contains the package entity used to be an intermediate between :class:`imagination.locator.Loccator`
and :class:`imagination.loader.Loader` and simulate the singleton class on the package in the Loader.
'''

from imagination.loader    import Loader
from imagination.exception import UnknownLoaderError

class Entity(object):
    '''
    Entity represents the package information, reference and instance of the reference.
    
    *id* is the service identifier (string).
    
    *loader* is a service loader which is an instance of :class:`imagination.loader.Loader`.
    
    *args* and *kwargs* are parameters used to instantiate the service.
    
    If the loader is not an instance of :class:`imagination.loader.Loader` or any classes based on
    :class:`imagination.loader.Loader`, the exception :class:`imagination.exception.UnknownLoaderError` will be thrown.
    
    .. note::
        This class is to similar to the decorator :meth:`tori.decorator.common.singleton` and
        :meth:`tori.decorator.common.singleton_with` from Tori Framework, except that it is not
        a singleton class and so any arbitrary class referenced by the *loader* only lasts as
        long as the entity lives.
    '''
    
    def __init__(self, id, loader, *args, **kwargs):
        if not isinstance(loader, Loader):
            raise UnknownLoaderError, 'Expected a service loader.'
        
        self._id       = id
        self._loader   = loader
        self._args     = args
        self._kwargs   = kwargs
        self._instance = None
    
    def id(self):
        ''' Get the entity ID. '''
        return self._id
    
    def loader(self):
        ''' Get the package loader. '''
        return self._loader
    
    def argument_list(self):
        ''' Get the argument list. '''
        return self._args
    
    def argument_dictionary(self):
        ''' Get the argument dictionary. '''
        return self._kwargs
    
    def activated(self):
        '''
        Check if the entity is already activated.
        
        This will also inspects if the entity already loads a singleton instance into the memory.
        '''
        return self._instance is not None
    
    def instance(self):
        ''' Get the singleton instance of the class referred in the loader. '''
        if not self._instance:
            self._instance = self._loader.package()(*self._args, **self._kwargs)
        
        return self._instance
