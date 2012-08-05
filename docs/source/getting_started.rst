Getting Started
===============

:Author: Juti Noppornpitak

As I am a lazy lad, I will guide you, the reader, through the framework with this example.

.. note::
    This example is based on the actual test.

First step
----------

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

Manager

.. note::
    This document is incomplete. Writting in progress.