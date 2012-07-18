'''
:Author: Juti Noppornpitak
:Availability: 1.5

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

import inspect

from imagination.exception import MisplacedValidatorError

def restrict_type(*restricted_list, **restricted_map):
    '''
    The method decorator to validate the type of inputs given to the method.
    
    :param `restricted_list`: the list of types to restrict the type of each
                              parameter in the same order as the parameter given
                              to the method.
    :param `restricted_map`:  the map of types to restrict the type of each
                              parameter by name.
    '''
    def inner_decorator(reference):
        if isinstance(reference, type) or not callable(reference):
            raise MisplacedValidatorError,\
                'Can only be used with callable objects, e.g., functions, class methods, instance methods and static methods.'

        params   = inspect.getargspec(reference).args
        is_class = params and params[0] == 'self'

        if is_class:
            def new_reference(self, *args, **kwargs):
                __validate_type(restricted_list, restricted_map, args, kwargs)

                return reference(self, *args, **kwargs)
        else:
            def new_reference(*args, **kwargs):
                __validate_type(restricted_list, restricted_map, args, kwargs)

                return reference(*args, **kwargs)

        return new_reference

    return inner_decorator

def __validate_type(allowed_list, allowed_dictionary, argument_list, argument_dictionary):
    allowed_list = allowed_list[:len(argument_list)]
    reference    = None

    try:
        for index in range(len(allowed_list)):
            expected_type = allowed_list[index]
            reference     = argument_list[index]

            if not expected_type:
                continue

            assert __assert_type(reference, expected_type),\
                expected_type.__name__

        for key, expected_type in allowed_dictionary.iteritems():
            reference = argument_dictionary[key]

            if key not in argument_dictionary:
                continue

            assert __assert_type(reference, expected_type),\
                expected_type.__name__

    except AssertionError, e:
        raise TypeError, 'Excepted %s, given %s.' % (e.message, type(reference).__name__)

def __assert_type(instance, expected_type):
    if not isinstance(expected_type, type):
        raise TypeError, 'The expected type must be a type.'

    fallback_types = []

    if expected_type is unicode:
        fallback_types.append(str)
    elif expected_type is long:
        fallback_types.append(float)
        fallback_types.append(int)

    if isinstance(instance, expected_type):
        return True

    for fallback_type in fallback_types:
        if isinstance(instance, fallback_type):
            return True

    return False