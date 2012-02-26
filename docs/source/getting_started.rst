Getting Started
===============

:Author: Juti Noppornpitak

As I am a lazy lad, I will guide you, the reader, through the framework with this example.

.. note::
    This example comes straight out of the test.

Planning on using dummy.core
----------------------------

Suppose we have the module `dummy.core` with classes::

    class PlainOldObject(object):
        def __init__(self):
            pass
    
        def method(self):
            return 0

    class PlainOldObjectWithParameters(object):
        def __init__(self, a, b, do_multiply=True):
            self.a = a
            self.b = b
            self.d = do_multiply
    
        def method(self):
            r = self.d and self.a * self.b or self.a / self.b
        
            return r

    class DependencyInjectableObjectWithClass(object):
        def __init__(self, reference):
            self.r = reference
            self.i = reference()

    class DependencyInjectableObjectWithEntity(object):
        def __init__(self, entity):
            self.e = entity

What about the code base?
-------------------------

Then, we also have the code base as followed::

    project/
        main.py <-- this is the main script to bootstrap and run this app.
        imagination.xml
        controllers.py
        views.py
        models.py

where at least one of non-main python scripts uses ``dummy.core``.

Prettify the code
-----------------

Assume that the code is really messy.

In order not to declare dependencies in the main code base, first, we added the following code to ``main.py``::

    from imagination.locator import Locator
    im_locator = Locator()
    im_locator.load_xml('imagination.xml')

Lovely! This will make ``im_locator`` aware of any classes defined in the XML file. But what would the file be like? The following can help you.

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <!-- Location: project/imagination.xml -->
    <imagination>
        <entity id="poo" class="dummy.core.PlainOldObject"></entity>
        <entity id="poow-1" class="dummy.core.PlainOldObjectWithParameters">
            <param name="a" type="int">2</param>
            <param name="b" type="float">3</param>
            <param name="do_multiply" type="bool">false</param>
        </entity>
        <entity id="poow-2" class="dummy.core.PlainOldObjectWithParameters">
            <param name="a" type="int">5</param>
            <param name="b" type="int">7</param>
        </entity>
        <entity id="dioc" class="dummy.core.DependencyInjectableObjectWithClass">
            <param name="reference" type="class">dummy.core.PlainOldObject</param>
        </entity>
        <entity id="dioe" class="dummy.core.DependencyInjectableObjectWithEntity">
            <param name="entity" type="entity">poow-1</param>
        </entity>
    </imagination>

.. note::
    The DTD is not ready yet.

This XML file defines 5 entities identified as ``poo``, ``poow-1``, ``poow-2``, ``dioc`` and ``dioe``.

An ``entity`` block always only has two attributes:

========= ================================================================================================================
Attribute Description
========= ================================================================================================================
``id``    the identifier of the entity used as a key in retrieving from the locator (:class:`imagination.locator.Locator`)
``class`` the class of the instance encapsulated by the entity (:class:`imagination.entity.Entity`)
========= ================================================================================================================

As you can see, each ``<entity>`` may have ``<param>`` where:

* the attribute ``name`` is required and represents the name of the arguments of the class,
* and the attribute ``type`` is optional and represents the type of the value, which is currently supported for:

========= =========================================
Type Name Data Type
========= =========================================
unicode   Unicode (default)
bool      Boolean [#pt1]_
float     Float
int       Integer
reference Class reference [#pt2]_
entity    :class:`imagination.entity.Entity` [#pt3]_
========= =========================================

Hopefully, ``im_locator`` in ``main.py`` is accessible by others.

.. note::
    At this point, normally entities are not instantiated unless any parameters of
    an entity are of type ``reference`` [#pt2]_ and ``entity`` [#pt3]_.

Now, time to use the imagination
--------------------------------

In any files, first, added::

    from main.py import im_locator as locator

To use what we already defined, use::

    locator.get('poow-1') # 'poow-1' is an identifier of the entity.

.. rubric:: Footnotes

.. [#pt1] Only any variations (letter case) of the word 'true' are considered as ``True``.
.. [#pt2] The module and package specified as the value of ``<param>`` is loaded when :meth:`Locator.load_xml` is called.
.. [#pt3] The encapsulated instance of the entity specified as the value of ``<param>`` is instantiated when :meth:`Locator.load_xml` is called.