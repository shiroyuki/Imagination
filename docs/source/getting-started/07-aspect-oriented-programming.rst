Aspect-oriented Programming with Entities
#########################################

.. warning::

    This is an testing/unstable feature. This documentation take precedence.

Now, you know how to define all types of entities. As **Imagination** is also a
framework to let you do the aspect-oriented programming with ease, this section
will show you how you can do that with just XML configuration files.

How can you do that?

Suppose you have the following scenarios.


.. code-block:: cucumber

    Given entity "bob" orders "Pad Thai"
     Then entity "server" passes on the order to entity "chef"
      And entity "chef" cooks the order.

    Given entity "chef" finishes cooking
      And entity "server" delivers the order to "bob"
      And before entity "bob" can eat, the entity must wash hands.

    Given entity "entity" makes unavailable order
     Then entity "server" apologizes

From the following scenarios, you can translate into the XML configuration.


.. code-block:: xml

    <imagination>
        <entity id="bob" class="...">
            <!-- ... (assumed the paramaters are defined) ... -->

            <interception before="bob" do="eat" with="sanitize_hands"/>
            <!--
                bob.order()          -> str
                bob.eat(order)       -> None
                bob.sanitize_hands() -> None
            -->
        </entity>
        <entity id="server" class="...">
            <!-- ... (assumed the paramaters are defined) ... -->

            <interception after="bob" do="order" with="relay_order"/>
            <!--
                server.relay_order(order):
                    chef.cook(order)
            -->

            <interception after="chef" do="cook" with="deliver"/>
            <!--
                server.deliver(order):
                    bob.eat(order)
            -->

            <interception error="bob" do="error" with="apologize"/>
            <!--
                server.apology(order)
                    server.say('We do not have this at the moment.', bob)
            -->
        </entity>
        <entity id="chef" class="...">
            <!-- ... (assumed the paramaters are defined) ... -->
            <!--
                chef.cook(order) -> str
            -->
        </entity>
    </imagination>

At this point, when you execute ``assembler.core.get('bob').order()``, the
execution chain will be executed as specified.

From this example, to run code **before executing some code**, from "bob"

.. code-block:: xml

    <interception before="bob" do="eat" with="sanitize_hands"/>

means "before **bob** executes ``eat``, **bob** executes ``sanitize_hands`` with
the parameters for executing ``eat``".

Or from "server", to run code **after executing some code**, from "server",

.. code-block:: xml

    <interception after="chef" do="cook" with="deliver"/>

means "after **chef** executes ``cook``, **server** executes ``deliver`` with
the result from executing ``cook``".

Or from "server", to run code **when an uncaught exception occurs while
executing some code**, from "server",

.. code-block:: xml

    <interception error="bob" do="order" with="apologize"/>

means "while **bob** executes ``order``, if an error occurs, **server** executes
``apologize`` with the parameters for executing ``order``".

.. tip::

    For more information about the DTD of the configuration file, please check
    out `the DTD <https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd>`_
    on GitHub.

Next step? :doc:`0x-diy`.
