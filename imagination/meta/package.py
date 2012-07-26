'''
:Author: Juti Noppornpitak
:Availability: 1.5
:Usage: Internal

The module contains the data structure of method interception to aid the analysis
and construction of the loaders and entities based on the configuration.

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

from imagination.decorator.validator import restrict_type

class Interceptor(object):
    '''
    The metadata for an interceptor.
    '''
    def __init__(self):
        self._id         = None
        self._action     = None
        self._parameters = None

class Parameter(object):
    '''
    Parameter Package represents the parameter of arguments as
    a list and a dictionary to any callable objects (e.g.,
    constructor and methods).

    :param `largs`:  a list of arguments
    :param `kwargs`: a dictionary of arguments
    '''

    @restrict_type(list, dict)
    def __init__(self, largs=None, kwargs=None):
        self.largs  = largs  or []
        self.kwargs = kwargs or {}