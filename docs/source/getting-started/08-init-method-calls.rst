Method Calls on Initialization
##############################

.. versionadded:: 2.6

.. warning::

    This is an experimental support in **Imagination 2.6** and designed to work only with
    **Python 3.5** or newer.

In some situations, you may want to call some methods upon successful initialization/instantiation.

Suppose we have a code like the following.

.. code-block:: python

    import threading

    class Counter(object):
        def __init__(self):
            self.debug_mode = False
            self.ping_count = 0

        def ping(self):
            self.ping_count += 1

        def enable_debug_mode(enabled):
            self.debug_mode = enabled or False

    class App(object):
        def __init__(self):
            self.counter = None

        def set_counter(self, counter):
            self.counter = counter

        def listen(self):
            while True:
                self.counter.ping()

        def passively_listen(self):
            listener = threading.Thread(target = self.listen, daemon = True)
            listener.start()

We want to define entities in a way that:

* ``app`` will start listening in the background with ``passively_listen`` upon instantiation but
  we DO NOT want to call the method inside ``__init__``.

.. code-block:: xml

    <entity id="app" class="app.App">
        <call method="passively_listen"/>
    </entity>

* Once the entity ``counter`` is instantiated, the main container will call the method
  ``set_counter`` from the entity ``app`` with itself.

.. code-block:: xml

    <entity id="counter" class="app.Counter">
        <call method="enable_debug_mode">
            <param type="bool" name="enabled">true</param>
        </call>
        <call method="set_counter" from="app">
            <param type="entity" name="counter">self</param>
            <!-- NOTE "self" refers to "counter". -->
        </call>
    </entity>
