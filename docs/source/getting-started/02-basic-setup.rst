Basic Setup
###########

Suppose your app looks like this.

.. code-block:: text

    root_dir/
        app/
            __init__.py
        containers.xml
        main.py

``containers.xml``, which is the configuration of the framework, looks like this:

.. code-block:: xml

    <imagination>
    </imagination>

.. tip::

    For more information about the DTD of the configuration file, please check
    out `the DTD <https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd>`_
    on GitHub.

``main.py``, which is the main script, looks like this:

.. code-block:: python

    from imagination.assembler.core import Assembler

    assembler = Assembler()
    assembler.load('containers.xml')

    # TODO do something

.. tip::

    Please remember that you can load multiple XML configuration files as shown
    in the following example:

    .. code-block:: python

        assembler.load('config1.xml', 'config2.xml', ...)


Before you go further into the rabbit hole, you might want to keep :doc:`../definitions` handly.

Next step? :doc:`03-create-new-entity`.
