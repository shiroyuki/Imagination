# -*- coding: utf-8 -*-

'''
:Author: Juti Noppornpitak
:Version: 1.5
:Usage: Internal

The module contains the classes used for interceptable actions/methods of any
instance of :class:`imagination.entity.Entity`.

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

from imagination.decorator.validator import restrict_type, SpecialType
from imagination.meta.interception   import Interception
from imagination.meta.package        import Parameter

class EventType(object):
    '''
    Type of intercepting events
    '''

    pre_action     = 'before'
    ''' Event before the execution that doesn't care about the input given to the action. '''

    pre_condition  = 'pre'
    ''' Event before the execution that only concerns about the input given to the action. '''

    post_condition = 'post'
    ''' Event after the execution that only concerns about the returned value from the action. '''

    post_action    = 'after'
    ''' Event after the execution that doesn't care about the returned value from the action. '''

class Action(object):
    '''
    Method wrapper for intercepting actions
    '''
    @restrict_type(SpecialType.function)
    def __init__(self, f):
        self.__doc__    = f.__doc__
        self.__name__   = f.__name__
        self._reference = f
        self.__pre_actions  = []
        self.__post_actions = []

    def __call__(self, *args, **kwargs):
        parameters = Parameter(args, kwargs)

        self.__run_pre_events(parameters)

        feedback = self.reference(*parameters.largs, **parameters.kwargs)
        feedback = self.__run_post_events(feedback)

        return feedback

    @property
    def name(self):
        ''' Name of the action '''
        return self.__name__

    @property
    def reference(self):
        ''' Reference of the action '''
        return self._reference

    @restrict_type(Interception)
    def register(self, interception):
        event = str(interception.event)

        if event in [EventType.pre_action, EventType.pre_condition]:
            self.__pre_actions.append(interception)
            return

        if event in [EventType.post_action, EventType.post_condition]:
            self.__post_actions.append(interception)
            return

        raise ValueError('The event "%s" is not recognized.' % event)

    @restrict_type(Interception)
    def __retrieve_callback(self, interception):
        callback = interception.handler.interface

        # cache callback?

        if not callable(callback):
            raise NonCallableError('%s.%s is not callable' % (
                interception.handler.id,
                interception.handler.method_name
            ))

        return callback

    @restrict_type(Parameter)
    def __run_pre_events(self, parameters):
        for interception in self.__pre_actions:
            callback = self.__retrieve_callback(interception)

            if interception.event == EventType.pre_action:
                interception.handler.engage()
                continue

            if interception.event == EventType.pre_condition:
                callback(*parameters.largs, **parameters.kwargs)
                continue

            raise ValueError('The event "%s" is not recognized.' % interception.event)

    def __run_post_events(self, feedback):
        for interception in self.__post_actions:
            callback = self.__retrieve_callback(interception)

            if interception.event == EventType.post_action:
                interception.handler.engage()
                continue

            if interception.event == EventType.post_condition:
                feedback = callback(feedback)
                continue

            raise ValueError('The event "%s" is not recognized.' % interception.event)

        return feedback
