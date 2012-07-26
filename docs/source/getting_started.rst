Getting Started
===============

:Author: Juti Noppornpitak

As I am a lazy lad, I will guide you, the reader, through the framework with this example.

.. note::
    This example is based on the actual test.

Planning on using dummy.core
----------------------------

Suppose we have the module ``restaurant`` with classes::

    class Conversation(object):
        logs = []

        @staticmethod
        def log(actor, context):
            Conversation.logs.append('%s: %s' % (actor.__class__.__name__, context))

    class Alpha(object):
        def __init__(self, accompany):
            self.accompany = accompany
            self.name      = self.__class__.__name__

        def call_accompany(self):
            self.accompany.acknowledge()

            return self.accompany

        def order(self, item):
            Conversation.log(self, 'order "%s"' % item)
            return item

        def speak_to_accompany(self, context):
            Conversation.log(self, 'speak to %s, "%s"' % (self.accompany.__class__.__name__, context))

        def wash_hands(self):
            Conversation.log(self, 'wash hands')

        def speak(self, context):
            Conversation.log(self, 'say, %s' % context)

        def confirm(self, order):
            Conversation.log(self, 'confirm for %s' % order)

    class Beta(object):
        def __init__(self):
            self.name = self.__class__.__name__

        def acknowledge(self):
            Conversation.log(self, 'acknowledge')

    class Charlie(object):
        def __init__(self):
            self.name = self.__class__.__name__

        def introduce(self):
            Conversation.log(self, 'introduce itself as "%s"' % self.name)

            return self.name

        def cook(self):
            Conversation.log(self, 'cook')

        def serve(self):
            Conversation.log(self, 'serve')

        def respond(self, response):
            Conversation.log(self, 'respond "%s"' % response)

        def repeat(self, feedback):
            Conversation.log(self, 'repeat "%s"' % feedback)
            return feedback

What about the code base?
-------------------------

Then, we also have the code base as followed::

    stage-app/
        main.py <-- this is the main script to bootstrap and run this app.
        imagination.xml
        restaurant.py

where ``main.py`` has the following content while using Imagination 1.5 or higher::

    # Imagination 1.5+
    from imagination.helper.assembler import Assembler
    from imagination.helper.data      import Transformer
    from imagination.locator          import Locator

    locator     = Locator()              # pretty much like entity manager
    transformer = Transformer(locator)   # data transformer as a mandatory extension for Assembler
    assembler   = Assembler(transformer)

    assembler.load('imagination.xml')

or the following one with Imagination 1.0::

    # Imagination 1.0
    from imagination.locator import Locator

    locator = Locator()
    locator.load_xml('imagination.xml')

.. warning::
    :meth:`imagination.locator.Locator.load_xml` is deprecated in version 1.5
    and the concept of aspect-oriented programming (AOP) has been introduced
    since version 1.5.

.. note::
    This document is incomplete. Writting in progress.