Reserved Entity Identifiers
###########################

There are a few reserved entity identifiers.

* ``container`` refers to the main container (:class:`imagination.core.Imagination`).
* ``self`` refers to the ID of the closest entity and is ONLY used within the context of ``<interception/>``
  and ``<call/>`` (added in v2.6). For example, from an example in :doc:`08-init-method-calls`, the
  definition of the initial method call uses ``self`` to refer to the entity ``counter``.

.. code-block:: xml

    <entity id="counter" class="app.Counter">
        <!-- omitted -->
        <call method="set_counter" from="app">
            <param type="entity" name="counter">self</param><!-- NOTE "self" refers to "counter". -->
        </call>
    </entity>
