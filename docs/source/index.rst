.. Imagination documentation master file, created by
   sphinx-quickstart on Sat Feb 25 20:41:55 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Imagination
###########

:Copyright: Juti Noppornpitak
:Author:    Juti Noppornpitak
:License:   MIT

**Imagination** is a reusable component and aspect-oriented programming
framework which encapsulates an object into a single object, called
**containers**, inspired by many frameworks, e.g., Symfony Framework in PHP and
Spring Framework in Java.

.. note::

    This documentation is backward compatible from version 2.0 to 3.x. Version 1.x is no longer supported.

Why do you want to consider using this framework?
=================================================

* Your code always requires to instantiate a large number of objects and
  maintain the dependencies between objects and the order of instantiations.
  *In the other words, your have to manage the order of dependency injection manually*
* You want to instantiate a set of objects but do not want to put them in the
  scope of the module that your code instantiates.
* You want to implement the aspect-oriented programming (AOP), which allows
  you to write a simple, clean, testable, and maintainable code.

Understand why you need this?
=============================

If you get confused, please check out the presentation `How to write maintainable code without tests <http://www.slideshare.net/jutinoppornpitak/how-to-write-maintainable-code-without-tests>`_ at PyCon Canada 2016 for more information.

Please note that some terms are slightly different as this library is made before I got a little bit smarter.

:Entity: A **service**
:Core: An **injector**

How to Install
==============

:With PIP:   pip install imagination
:With Make:  make install
:With `setup.py`: python setup.py install

Next many steps
===============

.. toctree::
   :maxdepth: 1
   :glob:

   getting-started/index
   *

More resources
==============

* `XML DTD for the configuration file <https://github.com/shiroyuki/Imagination/blob/v2-dev/imagination.dtd>`_
* `Source Code on GitHub <https://github.com/shiroyuki/Imagination>`_

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
..
