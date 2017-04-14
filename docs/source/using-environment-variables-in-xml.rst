Using environment variables in XML configuration
################################################

.. versionadded:: Imagination 2.5

    New enhancement :)

You can refer to any environment variables in the XML configuration file. Here is how you can do it.

Suppose we have this configuration.

.. code-block:: xml

    <imagination>
        <entity id="parser" class="app.Server">
            <param type="str" name="run_as">data_service</param>
            <param type="str" name="storage_path">/storage</param>
        </entity>
    </imagination>

However, we would like to be able to make the running user and the storage path configurable. What
we can do now is to refer to configuration via **environment blocks**.

.. code-block:: xml

    <imagination>
        <entity id="parser" class="app.Server">
            <param type="str" name="run_as">{ $USER }</param>
            <param type="str" name="storage_path">{ $STORAGE_PATH or "/" }storage</param>
        </entity>
    </imagination>

.. note::

    The syntax is ``{ $<environment_name> [or <default_value> ]}`` where:

    * ``<environment_name>`` can only contains ``A-Z,a-z,0-9,_,.`` (i.e., valid environment variable names),
    * ``<default_value>`` is JSON-encode-able **only** of type ``int``, ``float``, and ``str``,
    * there may be any spaces after ``{`` and before ``}``,
    * there must be at least one space before and after ``or``.

When Imagination parses the value of parameter or item, the assembler will replace the environment
block *with the environment variable or the default value (if defined)* before evaluate the final
value into any defined data type.

.. tip::

    If the environment variable is undefined and the default value is not set, e.g., ``{ $USER }``,
    Imagination will raise ``imagination.exc.UnknownEnvironmentVariableError``.
