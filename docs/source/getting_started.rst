Getting Started
===============

:Author: Juti Noppornpitak

As I am a lazy lad, I will guide you, the reader, through the framework with this example.

.. note::
    This example is based on the actual test.

Simple Setup
------------

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

    # Imagination

.. warning::
    :meth:`imagination.locator.Locator.load_xml` is deprecated in version 1.5.

Advanced Setup with Aspect-oriented Programming
-----------------------------------------------

.. warning::
    This section is applicable with Imagination 1.5 or higher.

First of all, let's define two actors (entity) in this story: **alpha** as a
customer and **charlie** as a chef/server.

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <imagination>
        <entity id="alpha" class="restaurant.Alpha">
            <param type="entity" name="accompany">beta</param>
        </entity>
        <entity id="charlie" class="restaurant.Charlie"/>
    </imagination>

With this, in the code, we can get any of the actors by::

    alpha = locator.get('alpha') # to get "alpha".

Then, suppose that before **charlie** cooks, he needs to listen when customers
want to eat. In the old fashion way, we might have done.::

    # restaurant.py
    class Charlie(object): # entity "charlie"
        # anything before ...

        def cook(self):
            order = []

            order.append(alpha.order()) # "egg and becon"

            # do cooking...

        # anthing after ...

    # main.py
    locator.get('charlie').take_care(locator.get('alpha'))
    locator.get('charlie').cook()

or::

    # main.py
    locator.get('charlie').take_order(locator.get('alpha').order())
    locator.get('charlie').cook()

.. note::
    Assume that **charlie** has methods ``take_care`` or ``take_order``
    and **alpha** has a method ``order``.

Well, it works but Charlie needs to know **alpha**. What if there are more
people added into the story. Then, the code will become unnecessarily messy.
Let's apply AOP then.

By doing that, first, ``Charlie`` is slightly modified.

.. code-block:: python

    class Charlie(object): # entity "charlie"
        # anything before ...

        def cook(self):
            # do cooking...

        # anthing after ...

Then, in ``imagination.xml``, we now add **interceptions**.

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <imagination>
        <entity id="alpha" class="restaurant.Alpha">
            <param type="entity" name="accompany">beta</param>
            <interception before="charlie" do="cook" with="order">
                <param type="unicode" name="item">egg and becon</param>
            </interception>
        </entity>
        <entity id="charlie" class="restaurant.Charlie"/>
    </imagination>

Finally, in ``main.py``, we can just write::

    locator.get('charlie').cook()

On execution, assuming that **alpha** sends the order to the central queue,
**alpha** will intercept **before** **charlie** ``cook`` by ordering "egg and
becon". Then, **charlie** will take the order from the central queue.

.. note:: Read :doc:`api/helper.assembler` for the configuration specification.

Now, eventually, we have the cleaner code that do exactly what we want in the
more maintainable way.