Definitions used in this documentation
######################################

Terminology
===========

:Container/Core: the container of entities
:Entity: a reference to any kind of object
:Factorized entity: an entity created by a factory entity
:Lambda entity: a reference to a callable object
:Interception: an action where Imagination executes a code described in the configuration before, after the target method execution or when the method execution throws exceptions.

DTD for the XML configuration
=============================

:Source: https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd

.. code-block:: dtd

    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE imagination [
    <!ELEMENT imagination (entity|factorization|callable)*>
    <!-- [Regularentity] -->
    <!ELEMENT entity (param|interception)*>
    <!ATTLIST entity id ID #REQUIRED>
    <!-- Fully-qualified path to import -->
    <!ATTLIST entity class CDATA #REQUIRED>
    <!-- [Factorized entity] -->
    <!ELEMENT factorization (param|interception)*>
    <!ATTLIST factorization id ID #REQUIRED>
    <!-- Factory (entity) ID -->
    <!ATTLIST factorization with CDATA #REQUIRED>
    <!-- Factory method -->
    <!ATTLIST factorization call CDATA #REQUIRED>
    <!-- [Lambda entity] -->
    <!ELEMENT callable EMPTY>
    <!ATTLIST callable id ID #REQUIRED>
    <!-- Fully-qualified path to import -->
    <!ATTLIST callable with CDATA #REQUIRED>
    <!-- [Interception] -->
    <!ELEMENT interception EMPTY>
    <!-- Interceptable events where IDREF is the intercepting entity ID -->
    <!ATTLIST interception before IDREF #IMPLIED>
    <!ATTLIST interception after IDREF #IMPLIED>
    <!ATTLIST interception error IDREF #IMPLIED>
    <!-- Intercepted method name -->
    <!ATTLIST interception do CDATA #REQUIRED>
    <!-- Intercepting method name -->
    <!ATTLIST interception with CDATA #REQUIRED>
    <!-- [Parameter Definition] -->
    <!ELEMENT param (item*|#PCDATA)>
    <!-- Parameter Name -->
    <!ATTLIST param name CDATA #REQUIRED>
    <!-- Parameter Type -->
    <!ATTLIST param type (unicode|str|bool|float|int|class|entity|set|list|tuple|dict) #REQUIRED>
    <!-- [List/Dictionary Item Definition] -->
    <!ELEMENT item (item*|#PCDATA)>
    <!-- Dictionary Key (Optional) -->
    <!ATTLIST item name CDATA #IMPLIED>
    <!-- Item Type -->
    <!ATTLIST item type (unicode|str|bool|float|int|class|entity|set|list|tuple|dict) #REQUIRED>
    ]>
