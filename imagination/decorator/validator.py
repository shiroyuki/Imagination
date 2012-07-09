'''
:Author: Juti Noppornpitak

The module contains reusable input validators.

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

from imagination.exception import MisplacedValidatorError

def allowed_type(*allowed_list, **allowed_dictionary):
    '''
    The method decorator to validate the input given to the reference.
    '''
    def inner_decorator(reference):
        if isinstance(reference, type) or not callable(reference):
            raise MisplacedValidatorError, 'Can only be used with callable objects, e.g., functions, class methods, instance methods and static methods.'
        
        return StrictTypedCallableObject(reference, *allowed_list, **allowed_dictionary)

    return inner_decorator

class SpecialType(object):
    function = 'function' # function representative

class StrictTypedCallableObject(object):
    def __init__(self, function, *allowed_list, **allowed_dictionary):
        self.function     = function
        self.allowed_list = allowed_list
        self.allowed_dictionary = allowed_dictionary

    def __call__(self, *largs, **kwargs):
        allowed_list = self.allowed_list[:len(largs)]

        try:
            for index in range(len(allowed_list)):
                if not allowed_list[index]:
                    continue

                kind = allowed_list[index]

                assert isinstance(largs[index], kind), kind.__name__

            for key, kind in self.allowed_dictionary.iteritems():
                if key not in kwargs:
                    continue

                assert isinstance(kwargs[key], kind), kind.__name__
        except AssertionError, e:
            raise TypeError, e.message

        return self.function(*largs, **kwargs)