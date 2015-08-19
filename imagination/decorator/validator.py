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

try:
    from inspect import getfullargspec
except ImportError as e:
    # Fall back to Python 2.7 mode
    from inspect import getargspec as getfullargspec

import sys

from imagination.exception import MisplacedValidatorError

_disable_decorator = 'sphinx' in sys.modules

class SpecialType(object):
    function = 'type:function'

def restrict_type(*restricted_list, **restricted_map):
    '''
    The method decorator to validate the type of inputs given to the method.

    :param `restricted_list`: the list of types to restrict the type of each
                              parameter in the same order as the parameter given
                              to the method.
    :param `restricted_map`:  the map of types to restrict the type of each
                              parameter by name.

    When the input fails the validation, an exception of type :class:`TypeError`
    is throw.

    There are a few exceptions:
     * If the given type is ``None``, there will be no restriction.
     * If the given type is ``long``, the value of ``int`` and ``float`` are also valid.
     * If the given type is ``unicode``, the valud of ``str`` is also valid.

    .. warning:: In Imagination 1.6, types ``unicode`` and ``long`` are no longer have fallback check in order to support Python 3.3.

    .. code-block:: python

        from imagination.decorator.validator import restrict_type

        # Example on a function
        @restrict_type(unicode)
        def say(context):
            print context

        class Person(object):
            # Example on a constructor
            @restrict_type(unicode, int)
            def __init__(self, name, age):
                self.name = name
                self.age  = age

                self.__friends = []

            # Example on an instance method
            @restrict_type(Person)
            def add_friend(self, person):
                self.__friends.append(person)

    '''
    def inner_decorator(reference):
        if _disable_decorator:
            return reference

        if isinstance(reference, type) or not callable(reference):
            raise MisplacedValidatorError(
                'Can only be used with callable objects, e.g., functions, class methods, instance methods and static methods.'
            )

        params   = getfullargspec(reference).args
        is_class = params and params[0] == 'self'

        if is_class:
            def new_reference(self, *args, **kwargs):
                __validate_type(restricted_list, restricted_map, args, kwargs)

                return reference(self, *args, **kwargs)
        else:
            def new_reference(*args, **kwargs):
                __validate_type(restricted_list, restricted_map, args, kwargs)

                return reference(*args, **kwargs)

        new_reference.__doc__ == reference.__doc__

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
                expected_type == SpecialType.function\
                and 'function'\
                or expected_type.__name__

        for key in allowed_dictionary:
            expected_type = allowed_dictionary[key]

            if key not in argument_dictionary:
                continue

            reference = argument_dictionary[key]

            if not expected_type:
                continue

            assert __assert_type(reference, expected_type),\
                expected_type.__name__

    except AssertionError as e:
        actual_type = e.message if 'message' in dir(e) else e

        raise TypeError('Argument #%s was excepting %s but %s has been given.' % (index, actual_type, type(reference).__name__))

def __assert_type(instance, expected_type):
    list_types = [list, tuple, set]

    callable_expected = expected_type == SpecialType.function
    instance_expected = isinstance(expected_type, type)

    if not callable_expected and not instance_expected:
        raise TypeError('The expected type must be a type.')

    fallback_types = []

    # If the callable is expected, validate if it is callable.

    if callable_expected:
        return callable(instance)

    # Now, validate the type of INSTANCE.
    if expected_type in list_types:
        fallback_types.extend(list_types)

    if type(instance) == expected_type or isinstance(instance, expected_type):
        return True

    for fallback_type in fallback_types:
        if type(instance) == fallback_type:
            return True

    return False
