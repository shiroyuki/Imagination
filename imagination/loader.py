'''
:Author: Juti Noppornpitak

The module contains the package loader used to improve code maintainability.

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

import re
import sys

class Loader(object):
    '''
    Package loader with lazy loading

    *path_to_package* is a string representing the package path.

    For example::

        # In this case, we load the default renderer of Tori framework.
        loader = Loader('tori.renderer.DefaultRenderer')
        # Then, instantiate the default renderer.
        renderer = loader.package()('app.views')

    '''
    def __init__(self, path_to_package):
        self._path         = path_to_package
        self._access_path  = re.split('\.', self._path)
        self._module_path  = '.'.join(self._access_path[:-1])
        self._module       = None
        self._package_name = self._access_path[-1]
        self._package      = None

    def name(self):
        ''' Get the name of the package. '''
        return self.module().__package__

    def module(self):
        ''' Get a reference to the module. '''
        return self._module or self._retrieve_module()

    def package(self):
        ''' Get a reference to the package. '''
        return self._package or self._retrieve_package()

    def filename(self):
        ''' Get the path to the package. '''
        return self.module().__file__

    def _retrieve_module(self):
        ''' Retrieve a module by the module path. '''

        try:
            if self._module_path not in sys.modules:
                __import__(self._module_path)

            self._module = sys.modules[self._module_path]

            return self._module
        except KeyError:
            return None

    def _retrieve_package(self):
        ''' Retrieve a package by the module path and the package name. '''

        __import__(self._module_path, fromlist=[self._package_name])

        return getattr(self.module(), self._package_name)
