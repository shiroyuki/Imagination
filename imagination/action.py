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

from inspect import getargspec
from imagination.meta.interception import Interception

class EventType(object):
    # event before the execution that doesn't care about the input given to the action.
    pre_action     = 'before'

    # event before the execution that only concerns about the input given to the action.
    pre_condition  = 'pre'

    # event after the execution that only concerns about the returned value from the action.
    post_condition = 'post'

    # event after the execution that doesn't care about the returned value from the action.
    post_action    = 'after'

class Action(object):
    def __init__(self, f):
        self.executed = False
        self.referrer = f.im_self
        self.reference = f
        self.reference_name = f.__name__
        self.__pre_actions  = []
        self.__post_actions = []

    def __call__(self, *args, **kwargs):
        self.__run_pre_events(*args, **kwargs)

        feedback = self.reference(*args, **kwargs)

        #feedback = self.__run_post_events(feedback)

        return feedback

    def register(self, interception):
        event = str(interception.event)

        if event in [EventType.pre_action, EventType.pre_condition]:
            self.__pre_actions.append(interception)
            return
        elif event in [EventType.post_action, EventType.post_condition]:
            self.__post_actions.append(interception)
            return

        raise ValueError, 'The event "%s" is not recognized.' % event

    def __retrieve_callback(self, interception):
        handler  = interception.handler.load()
        callback = handler.__getattribute__(interception.handling_action)

        # cache callback?

        if not callable(callback):
            raise NonCallableError, '%s.%s is not callable' % (
                interception.handler.id(),
                interception.handling_action
            )

        return callback

    def __run_pre_events(self, *args, **kwargs):
        for interception in self.__pre_actions:
            callback   = self.__retrieve_callback(interception)
            parameters = interception.handling_parameters

            if interception.event == EventType.pre_action:
                callback(*parameters.largs, **parameters.kwargs)
                continue
            elif interception.event == EventType.pre_condition:
                callback(*args, **kwargs)
                continue

            raise ValueError, 'The event "%s" is not recognized.' % interception.event

    def __run_post_events(self, feedback):
        for interception in self.__post_actions:
            callback   = self.__retrieve_callback(interception)
            parameters = interception.handling_parameters

            if interception.event == EventType.post_action:
                callback(*parameters.largs, **parameters.kwargs)
                continue
            elif interception.event == EventType.post_condition:
                feedback = callback(feedback)
                continue

            raise ValueError, 'The event "%s" is not recognized.' % interception.event

        return feedback
