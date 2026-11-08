Quick start
###########

The recommended way to use **Imagination** is the **standalone container** together
with the ``@registered`` decorator. No XML configuration file is required:
Imagination reads your constructor type hints and injects the services for you.

.. code-block:: python

    from __future__ import annotations

    from imagination.decorator.service import registered
    from imagination.standalone import use


    @registered()
    class DataAdapter:
        def fetch(self) -> str:
            return "Hello from Imagination"


    @registered()
    class DataService:
        def __init__(self, adapter: DataAdapter):
            self.adapter = adapter

        def do_something(self) -> str:
            return self.adapter.fetch()


    service = use(DataService)
    assert service.do_something() == "Hello from Imagination"
    assert use(DataService) is service

``@registered()`` declares a **singleton** service without instantiating it. On the
first request Imagination creates ``DataAdapter`` and injects it into
``DataService`` using the constructor's type hint. Subsequent requests reuse the
same instances. Import the modules that contain the decorated classes before you
request their services.

Retrieving services
===================

``use(ServiceClass)`` (since v3.4) is a typed shortcut for
``container.get(ServiceClass)`` and lets IDEs and type checkers infer the service
type:

.. code-block:: python

    from imagination.standalone import container

    assert container.get(DataService) is service

Configuring dependencies
=========================

Required constructor arguments annotated with a registered service class are wired
automatically. Supply primitive values through the decorator's ``params`` argument
(``imagination.decorator.config``):

.. code-block:: python

    from imagination.decorator.config import Parameter


    @registered(params=[Parameter("Panda", name="name")])
    class NamedDataService:
        def __init__(self, name: str, adapter: DataAdapter):
            self.name = name
            self.adapter = adapter


    assert use(NamedDataService).name == "Panda"

Use ``Service`` from ``imagination.decorator.config`` for an explicit service
reference -- by class or ID, including injecting a concrete subclass into a
parameter annotated with its base class. Parameters that already have a default
value keep that default unless you configure them explicitly.

.. note::

    The XML configuration approach and aspect-oriented programming (AOP)
    interception remain available but are **legacy support**. New code should use
    the decorator approach documented here.

Next step? :doc:`03-standalone-and-decorators`.
