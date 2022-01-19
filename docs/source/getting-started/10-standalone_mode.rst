Standalone Mode and Component Decorators
########################################

The standalone mode is designed to allow developers to quickly use the Imagination container with
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
* service decorators (see the next section)

.. note::
    You can also load more configuration files later by calling :method:`imagination.standalone.load_config_file`.

Decorator API
*************

With the feedback from the community, in version 3.3, you can use decorators to configure services without the need to
learn how to write XML. This feature is now generally available for testing based on `the rolling feature ticket <https://github.com/shiroyuki/Imagination/issues/33>`_.

.. note:: It currently only supports entity-type service declarations.

How to use the API
==================

The decorator API will use a different set of terminologies, but similar to Angular's.

The decorator ``imagination.decorator.Component`` is to declare an entity-type service where the constructor's arguments
(AKA parameters) can be defined with the following object of these classes.

* ``imagination.decorator.config.Parameter`` is a primitive-type argument.
    * It is equivalent to ``<param/>`` for primitive-type arguments but without ``type`` attribute as the type is inferred from the value.
* ``imagination.decorator.config.Service`` is an injectable argument for components.
    * If you have an argument with type hint to a class, which is declared as a component, you can leave this blank as the container will automatically figure out which component to use by type hint.
* ``imagination.decorator.config.EnvironmentVariable`` is an argument whose value is derived from an environment variable.


Example
=======

Suppose we have ``Service1`` with no parameters.

.. code-block:: python

    from imagination.decorator import service

    @service.registered()
    class Service1:
        ...

Instead of registering in an XML file, we now can use ``@service.registered()`` to declare this as a (singleton) service.

Let's say we also have ``Service2`` that requires ``Service1``.

.. code-block:: python

    from imagination.decorator.config import Parameter, Service

    from app.service import Service1

    @service.registered([
        Parameter('Panda'),
        Service(Service1),
    ])
    class Service2:
        def __init__(self, name: str, s1: Service1):
            ...

But this is still mouthful to declare a service. You can simplify this by leaving ``Service`` alone.

.. code-block:: python

    @service.registered([Parameter('Panda')])
    class Service2:
        def __init__(self, name: str, s1: Service1):
            ...

To call components, you can simply use ``imagination.standalone.container``.

.. code-block:: python

    from imagination.standalone import container
    from app.service.s1 import Service1
    from app.service.s2 import Service2

    s1 : Service1 = container.get(Service1)  # --> Service1
    s2 : Service2 = container.get(Service2)  # --> Service2
