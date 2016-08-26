Define a lambda/callable entity
###############################

This step will help you define an entity referring to a callable object.

First, we create a callable ``write_json`` at ``app/func.py``:

.. code-block:: python

    def write_json(where, content):
        with open(where, 'w') as f:
            f.write(content)

Then, register this class as a lambda/callable entity in ``containers.xml``:

.. code-block:: xml

    <imagination>
        <!-- ... (omitted what are declared in the previous step) ... -->

        <callable
              id="happy_panda.write_to_file"
              method="func.write_json"/>

    </imagination>

Now, you have an entity called **happy_panda.write_to_file**.
We call this a lambda (or callable) entity (see more at :doc:`../definitions`).

.. warn::

    This type of entities does not allow parameters as the entity directly
    refers to a callable object.

How to work with the first-place report entity
==============================================

To refer the first-place report entity, for example, in ``main.py``, simply do:

.. code-block:: python

    # Omitted the code for main.py already shown above
    write = assembler.core.get('happy_panda.write_to_file')

.. tip::

    For more information about the DTD of the configuration file, please check
    out `the DTD <https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd>`_
    on GitHub.

Next step? :doc:`07-aspect-oriented-programming`.
