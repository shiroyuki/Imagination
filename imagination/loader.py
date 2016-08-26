# v1 and v2
"""
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

"""

import re
import importlib
import sys
from imagination.helper import retrieve_module

class OnDemandProxy(object):
    """On-demand Proxy

    .. codeauthor:: Juti Noppornpitak <juti_n@yahoo.co.jp>
    .. versionadded:: 1.6

    .. warning:: experimental feature
    """
    def __init__(self, loader):
        self.__loader = loader

    def __call__(self, *args, **kwargs):
        return self.__loader.package

class Loader(object):
    """Package loader with lazy loading

    *path_to_package* is a string representing the package path.

    For example::

        # In this case, we load the default renderer of Tori framework.
        loader = Loader('tori.renderer.DefaultRenderer')
        # Then, instantiate the default renderer.
        renderer = loader.package('app.views')

    """
    def __init__(self, path_to_package):
        self._path         = path_to_package
        self._access_path  = re.split('\.', self._path)
        self._module_path  = '.'.join(self._access_path[:-1])
        self._module       = None
        self._package_name = self._access_path[-1]
        self._package      = None

        self.on_demand_package = OnDemandProxy(self)

    @property
    def name(self):
        ''' Get the name of the package. '''
        return self.module.__package__

    @property
    def module(self):
        ''' Get a reference to the module. '''
        if not self._module:
            self._module = retrieve_module(self._module_path)

        return self._module

    @property
    def package(self):
        ''' Get a reference to the package. '''
        if not self._package:
            self._package = self._retrieve_package()

        return self._package

    @property
    def filename(self):
        ''' Get the path to the package. '''
        return self.module.__file__

    def _retrieve_package(self):
        ''' Retrieve a package by the module path and the package name. '''

        target_module = self.module

        # Either built-in class or a file.
        if '.' not in self._path:
            try:
                importlib.import_module(self._path)

                return getattr(target_module, self._path)
            except ImportError as exception:
                return eval(self._path)
                # NOP; assume that the request path is a built-in module.

            return

        try:
            __import__(self._module_path, fromlist=[self._package_name])
        except TypeError as exception:
            raise ImportError('Unable to import {}.{} as {}'.format(
                self._module_path, self._package_name, exception
            ))

        try:
            return getattr(target_module, self._package_name)
        except AttributeError as exception:
            raise ImportError('Module \'{}\' has no reference to \'{}\', except {}.'.format(
                target_module.__name__, self._package_name, ', '.join(dir(target_module))
            ))
