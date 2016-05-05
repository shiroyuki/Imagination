Assembler
=========

The module contains the assembler to construct loaders and entities based on the configuration
and register to a particular locator.

XML Schema
----------

.. note::
    This is the master specification document for the configuration.

The schema is defined as followed::

    # Base

    <imagination>
        (ENTITY|FACTORIZATION|CALLABLE)*
    </imagination>

    ##########
    # Entity #
    ##########

    ENTITY = <entity id="ENTITY_ID"
                     class="ENTITY_CLASS"
                     (tags="...")?
                     (interceptable="(false|true)")?
             >
                 (CONSTRUCTOR_PARAMETER)*
                 (INTERCEPTION)*
             </entity>

    FACTORIZATION = <factorization
                          id="CREATED_ENTITY_ID"
                          with="FACTORY_ENTITY_ID"
                          call="FACTORY_ENTITY_METHOD"
                        >
                          (CONSTRUCTOR_PARAMETER)*
                        </factorization>

    CALLABLE = <callable
                  id="CREATED_ENTITY_ID"
                  method="IMPORTABLE_PATH_TO_CALLABLE"
                  static="(true|false)"
                >
                  (CONSTRUCTOR_PARAMETER)*
                </callable>

    # Initial Parameter
    INITIAL_PARAMETER     = CONSTRUCTOR_PARAMETER

    # Constructor's parameter and initial parameter
    CONSTRUCTOR_PARAMETER = <param type="PARAMETER_TYPE" name="PARAMETER_NAME">
                                (PARAMETER_VALUE|ENTITY_ID|CLASS_IDENTIFIER|ENTRY_ITEM*)
                            </param>
    ENTRY_ITEM = <item( name="DICT_KEY")? type="DATA_TYPE">DATA_VALUE</item>

    # See the section "Parameter Types" for PARAMETER_TYPE.

    #########
    # Event #
    #########

    EVENT=(before|pre|post|after)

    INTERCEPTION =  <interception EVENT="REFERENCE_ENTITY_IDENTIFIER"
                                  do="REFERENCE_ENTITY_METHOD"
                                  with="THIS_ENTITY_METHOD"
                    >
                        (INITIAL_PARAMETER)*
                    </interception>

where:

* ``ENTITY_ID`` is the identifier of the entity.
* ``ENTITY_CLASS`` is the fully-qualified class name of the entity. (e.g. ``tori.service.rdb.EntityService``)
* ``CREATED_ENTITY_ID`` is the factorized entity ID. (Added in Imagination 1.9)
* ``FACTORY_ENTITY_ID`` is the factory entity ID. (Added in Imagination 1.9)
* ``FACTORY_ENTITY_METHOD`` is the factory method. (Added in Imagination 1.9)
* ``option`` is the option of the entity where ``ENTITY_OPTIONS`` can have one
  or more of:

  * ``factory-mode``: always fork the instance of the given class.
  * ``no-interuption``: any methods of the entity cannot be interrupted.

* ``REFERENCE_ENTITY_IDENTIFIER`` is the reference's entity identifier
* ``REFERENCE_ENTITY_METHOD`` is the reference's method name
* ``THIS_ENTITY_METHOD`` is this entity's method name
* ``EVENT`` is where the ``REFERENCE_ENTITY_METHOD`` is intercepted.

  * ``before`` is an event before the execution of the method of the reference
    (reference method) regardless to the given arguments to the reference
    method.
  * ``pre`` is an event on pre-contact of the reference method and concerning
    about the arguments given to the reference method. The method of the entity
    (the intercepting method) takes the same paramenter as the reference method.
  * ``post`` is an event on post-contact of the reference method and concerning
    about the result returned by the reference method. The intercepting method
    for this event takes only one parameter which is the result from the
    reference method or any previous post-contact interceptors.
  * ``after`` is an event after the execution of the reference method regardless
    to the result reterned by the reference method.

Parameter Types
---------------

========= ==========================================
Type Name Data Type
========= ==========================================
unicode   Unicode (default)
bool      Boolean (bool) [#pt1]_
float     Float (float)
int       Integer (int)
class     Class reference [#pt2]_
entity    :class:`imagination.entity.Entity` [#pt3]_
set       Python's Set (set)
list      Python's List (list)
tuple     Python's Tuple (tuple)
dict      Python's Dictionary (dict)
========= ==========================================

.. versionadded:: 1.6
    Support for ``list``, ``tuple``, ``set``
    (`Issue #12 <https://github.com/shiroyuki/Imagination/issues/12>`_), and
    ``dict`` (`Issue #13 <https://github.com/shiroyuki/Imagination/issues/13>`_).

.. rubric:: Footnotes

.. [#pt1] Only any variations (letter case) of the word 'true' or 'false' are
          considered as a valid boolean value.
.. [#pt2] The module and package specified as the value of ``<param>`` is loaded
          when :meth:`Assembler.load` is executed.
.. [#pt3] The encapsulated instance of the entity specified as the value of
          ``<param>`` is instantiated when :meth:`Assembler.load`
          is executed or when the instance is given with a proxy (:class:`imagination.proxy.Proxy`).

Example
-------

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <imagination>
        <entity id="alpha" class="dummy.lazy_action.Alpha">
            <param type="entity" name="accompany">beta</param>
            <interception before="charlie" do="cook" with="order">
                <param type="unicode" name="item">egg and becon</param>
            </interception>
            <interception pre="charlie" do="repeat" with="confirm"/>
            <interception before="charlie" do="serve" with="speak_to_accompany">
                <param type="str" name="context">watch your hand</param>
            </interception>
            <interception before="charlie" do="serve" with="wash_hands"/>
            <interception after="me" do="eat" with="speak">
                <param type="str" name="context">merci</param>
            </interception>
        </entity>
        <entity id="beta" class="dummy.lazy_action.Beta"/>
        <entity id="charlie" class="dummy.lazy_action.Charlie"/>
    </imagination>

API
---

.. automodule:: imagination.helper.data
    :members:

.. automodule:: imagination.helper.assembler
    :members:
