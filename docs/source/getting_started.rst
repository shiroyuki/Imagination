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

Entity Factorization
--------------------

.. versionadded 1.9

In Imagination 1.9, you can register a reusable entity instantiated by a factory
object. For example, you may have a code like this.

.. code-block:: python

    class Manager(object):
        def getWorkerObject(self, name):
            return Worker(name)

        def getDuplicationMethod(self, multiplier):
            def duplicate(value):
                return value * multiplier

            return duplicate

    class Worker(object):
        def __init__(self, name):
            self.name = name

        def ping(self):
            return self.name

If you want to be able to call the locator with an identity and get the result
of the object factorization, you may do so like the following example.

.. code-block:: xml

    <factorization id="worker.alpha" with="manager" call="getWorkerObject">
        <param name="name" type="str">Alpha</param>
    </factorization>

.. note:: The interception setting is the same as any normal entity.

.. note:: The factorization only supports forking objects.

Callback Proxy
--------------

.. versionadded:: 1.8

In case you want to execute something which cannot be registered with either an
XML file or manually instantiate the loader, you can use the Callback Proxy like
the following example::

    import os.path
    from imagination.loader import CallbackProxy

    def something(message):
        return os.path

    callback_proxy = CallbackProxy(something, 'lah')
    locator.set('cbp.something', callback_proxy)

When you call ``locator.get('cbp.something')``, you will get ``os.path``.