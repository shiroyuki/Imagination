Getting started
###############

**Imagination** is a reusable dependency injection framework. The recommended
approach is the **standalone container** together with the ``@registered``
decorator -- no XML configuration file is required.

.. warning::

    The **XML configuration** approach and **aspect-oriented programming (AOP)**
    interception are **legacy support**. They are retained for backward
    compatibility only; new code should use the standalone container and the
    ``@registered`` decorator.

Modern approach
===============

.. toctree::
    :maxdepth: 1
    :caption: Modern approach (recommended)

    01-installation
    02-quick-start
    03-standalone-and-decorators

Reference
=========

.. toctree::
    :maxdepth: 1
    :caption: Reference

    0t-reserved-entity-ids
    0x-diy

Legacy (deprecated)
===================

The pages in this section document the XML configuration approach and
aspect-oriented programming (AOP) interception. They are **legacy support** and
are retained for backward compatibility only.

.. toctree::
    :maxdepth: 1
    :caption: Legacy (deprecated)

    legacy-xml-basic-setup
    legacy-xml-entity
    legacy-xml-parameters
    legacy-xml-factorization
    legacy-xml-lambda
    legacy-aop
    legacy-init-method-calls
    legacy-env-vars-in-xml
