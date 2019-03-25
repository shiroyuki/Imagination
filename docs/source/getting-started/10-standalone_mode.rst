Standalone Mode
###############

.. versionadded:: Imagination 3.0.0a1
    This is a testing feature which is designed to be used with the coming
    companion feature to `allow service declarations with decorators <https://github.com/shiroyuki/Imagination/issues/33>`_.

    Please note that a testing feature is relative stable but may not be suitable
    for production use.

This is made to allow developers to quickly use the Imagination container with
any programming frameworks.

To use this, instead of using :class:`imagination.assembler.core.Assembler` in
:doc:`02-basic-setup`, you can just simply call.

.. code-block:: python

    from imagination.standalone import container

where ``container`` is an instance of :class:`imagination.core.Imagination`.

Imagination in the standalone mode only is currently designed to loaded
configuration files from the configuration file from (this the listed order):

* Wherever you define in the system environment variable ``IMAGINATION_CONF_FILEPATH``
* ``imagination.xml`` (from the current working directory)
* ``services.xml`` (from the current working directory)

You can also load more configuration files later by calling :method:`imagination.standalone.load_config_file`.