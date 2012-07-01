'''
:Author: Juti Noppornpitak

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
        This class is to similar to the decorator `tori.decorator.common.singleton` and
        `tori.decorator.common.singleton_with` from Tori Framework, except that it is not
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
        self._tags     = None
        self._locked   = False
    
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
    
    def lock(self):
        self._locked = True
    
    def locked(self):
        return self._locked
    
    def activated(self):
        '''
        Check if the entity is already activated.
        
        This will also inspects if the entity already loads a singleton instance into the memory.
        '''
        return self._instance is not None
    
    def tags(self, new_tags=None):
        '''
        Get the entity tags.
        
        :param `tags`: new tags as replacements
        '''
        if isinstance(new_tags, list) and not self.locked():
            self._tags = new_tags
        
        return self._tags or []
    
    def instance(self):
        ''' Get the singleton instance of the class defined for the loader. '''
        if not self._instance:
            self._instance = self.fork()
        
        return self._instance
    
    def fork(self):
        ''' Fork an instance of the class defined for the loader. '''
        return self._loader.package()(*self._args, **self._kwargs)
