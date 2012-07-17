# -*- coding: utf-8 -*-

'''
:Author: Juti Noppornpitak
:Version: 1.5

The module contains the package action used to be a wrapper or a decorator of
any methods or callable objects inside :class:`imagination.entity.Entity`
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

class Action(object):
    def __init__(self, f):
        self.f = f
        self.__pre_actions  = []
        self.__post_actions = []

    def __call__(self):
        self.__run_pre_events()

        feedback = self.f

        self.__run_post_events()

        return feedback

    def register_with_meta_interception(self):
        pass

    def register_pre_action(self, callback, *args, **kwargs):
        self.__pre_actions.append((callback, args, kwargs))

    def register_post_action(self, callback, *args, **kwargs):
        self.__post_actions.append((callback, args, kwargs))

    def __run_pre_events(self):
        pass

    def __run_post_events(self):
        pass

class Interceptor(object):
    '''
    Action Interceptor

    This class contains information about the callback, parameters used by
    the callback and the action configuration (:class:`Configuration`).
    '''
    def __init__(self, callback, parameter_package):
        self.callback          = callback
        self.parameter_package = parameter_package

class EventType(object):
    # event before the execution that doesn't care about the input given to the action.
    pre_action     = 'pre:before'

    # event before the execution that only concerns about the input given to the action.
    pre_condition  = 'pre:condition'

    # event after the execution that only concerns about the returned value from the action.
    post_condition = 'post:condition'

    # event after the execution that doesn't care about the returned value from the action.
    post_action    = 'post:action'
