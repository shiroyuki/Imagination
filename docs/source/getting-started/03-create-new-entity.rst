Register a new entity without parameters
########################################

Assume that we start from scratch. Let's create ``app/util.py``:

.. code-block:: python

    class Calculator(object):
        def add(self, a:int, b:int) -> int:
            return a + b

At this point, Imagination does not know about the calculator. To do so,
let's register an entity of an instance of `app.util.Calculator` in
``containers.xml``:

.. code-block:: xml

    <imagination>
        <entity id="calc" class="app.util.Calculator" />
    </imagination>

where **calc** is the entity ID.

.. note::

    In case you are confused, here is the equivalent code.

    .. code-block:: python

        from app.util import Calculator

        calc = Calculator()

    The key differences at this point are:

    * the object is not instantiated immediately and is instantiated when the
      the entity is requested/activated,
    * the object is living only in the scope of the container.

How to work with the calculator entity
======================================

To refer the calculator entity, for example, in ``main.py``, simply use
``calculator = assembler.core.get('calc')``

Now, to actually use the entity, let's add something to the end of ``main.py``.

.. code-block:: python

    # Omitted the code for main.py already shown above
    calculator = assembler.core.get('calc')
    result     = calculator.add(123, 456)  # -> int(579)

    print(calculator.add(123, 456))  # STDOUT: 579

So, as you can see, the entity works pretty much like a normal object, except
**the key differences mentioned earlier**.

Next step? :doc:`04-create-with-parameters`.
