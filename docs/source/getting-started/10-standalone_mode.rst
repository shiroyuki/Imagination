Standalone Mode and Service Decorators
########################################

Standalone mode provides a ready-to-use Imagination container for any Python
application or framework. Instead of setting up an
:class:`imagination.assembler.core.Assembler` as described in
:doc:`02-basic-setup`, import the shared container:

.. code-block:: python

    from imagination.standalone import container

``container`` is an instance of :class:`imagination.core.Imagination`.

Configuration files
*********************

On import, the standalone module loads existing XML configuration files in this
order:

* The path specified by the environment variable ``IMAGINATION_CONF_FILEPATH``.
* ``imagination.xml`` in the current working directory.
* ``services.xml`` in the current working directory.

All existing files in this list are loaded. If none exist, the container starts
without XML configuration. Decorators register services when their modules are
imported; they are not a configuration-file fallback.

To load additional XML configuration, call
:func:`imagination.standalone.load_config_file`:

.. code-block:: python

    from imagination.standalone import load_config_file

    load_config_file('extra-services.xml')

Decorator API
***************

Introduced in v3.3, the decorator API lets you declare entity-type services in
Python without writing XML. It implements the decorator-based registration
proposed in `issue #33 <https://github.com/shiroyuki/Imagination/issues/33>`_.
Use ``imagination.decorator.service.registered`` to register a class.

.. note::

    The decorator API supports entity-type service declarations. Other definition
    types, such as factory services, can still be configured with XML.

Registering and retrieving services
=====================================

The following example registers two singleton services. Imagination uses the
constructor's type hint to inject ``DataAdapter`` into ``DataService``:

.. code-block:: python

    from __future__ import annotations

    from imagination.decorator.service import registered
    from imagination.standalone import use


    @registered()
    class DataAdapter:
        def fetch(self) -> str:
            return 'Hello from Imagination'


    @registered()
    class DataService:
        def __init__(self, adapter: DataAdapter):
            self.adapter = adapter

        def do_something(self) -> str:
            return self.adapter.fetch()


    service = use(DataService)
    assert service.do_something() == 'Hello from Imagination'
    assert use(DataService) is service

Registration only defines how to create a service. The container creates the
service and its dependencies on the first request, then caches the instances.
Import modules containing decorated classes before requesting their services.

Since v3.4, :func:`imagination.standalone.use` provides a typed shortcut for
retrieving a registered service by class. Its return type allows IDEs and type
checkers to infer the service type. ``container.get`` remains available:

.. code-block:: python

    assert container.get(DataService) is service

``imagination.decorator.Component`` is an alias for ``registered``. The older
``imagination.decorator.service.Service`` decorator alias is deprecated since
v3.4; use ``registered`` in new code. This decorator alias is separate from the
``Service`` parameter described below.

Constructor parameters
========================

Use the ``params`` argument of ``@registered()`` to configure constructor
arguments explicitly:

* ``imagination.decorator.config.Parameter(value, name=None)`` supplies a value.
  It corresponds to an XML ``<param/>`` with its type inferred from the value.
* ``imagination.decorator.config.Service(service_cls_or_id, name=None)`` injects
  another service by its registered class or service ID.
* ``imagination.decorator.config.EnvironmentVariable`` reads a value from an
  environment variable, with optional parsing and a default value.

Without ``name``, entries map to constructor parameters by position. Using
``name`` selects a constructor parameter explicitly:

.. code-block:: python

    from imagination.decorator.config import Parameter, Service


    @registered(params=[
        Parameter('Panda', name='name'),
        Service(DataAdapter, name='adapter'),
    ])
    class NamedDataService:
        def __init__(self, name: str, adapter: DataAdapter):
            self.name = name
            self.adapter = adapter


    assert use(NamedDataService).name == 'Panda'

Required dependencies annotated with registered service classes are wired
automatically, so this example can also use
``@registered(params=[Parameter('Panda', name='name')])``. Primitive values such as
strings and integers must be supplied explicitly unless the constructor provides
a default.

Parameters with default values keep those defaults unless explicitly configured.
For example, ``adapter: DataAdapter = None`` stays ``None`` when no parameter is
provided. A required parameter annotated as ``Optional[DataAdapter]`` (with no
default value) is still wired to ``DataAdapter``.

Postponed annotations and subclasses
======================================

Auto-wiring and runtime type checks support annotations stored as strings by
``from __future__ import annotations``, as shown above. Imagination resolves
constructor annotations with ``typing.get_type_hints``. Referenced types must be
available in the defining module when the service is instantiated.

Explicit service references also allow subclass instances for parameters
annotated with a base class. To select a concrete implementation, register it and
pass ``Service(Implementation, name='dependency')`` in ``params``. A base-class
annotation alone does not select a registered subclass automatically.

Environment variables
=======================

Use ``EnvironmentVariable`` to configure a constructor argument from the
environment:

.. code-block:: python

    from imagination.decorator.config import EnvironmentVariable


    @registered(params=[
        EnvironmentVariable('APP_PORT', parse_value=int, name='port'),
    ])
    class Server:
        def __init__(self, port: int):
            self.port = port

By default, a missing variable raises ``KeyError``. To allow a missing variable,
set ``allow_default=True`` and provide ``default``. Values are read when the
decorator runs, so set environment variables before importing the service module.
If ``parse_value`` is provided, it runs before the default is applied and must
accept ``None`` when the variable is absent.

Service IDs
=============

By default, the service ID is the fully qualified class name. To register a
custom ID, supply ``id`` and use that ID for retrieval and explicit references:

.. code-block:: python

    @registered(id='app.adapter')
    class CustomAdapter(DataAdapter):
        pass


    @registered(params=[Service('app.adapter', name='adapter')])
    class CustomDataService:
        def __init__(self, adapter: DataAdapter):
            self.adapter = adapter


    adapter = container.get('app.adapter')
    assert use(CustomDataService).adapter is adapter

``use(CustomAdapter)`` and automatic wiring by ``CustomAdapter`` use the default
class-based ID; they do not look up the custom ID ``app.adapter``.
