.. Imagination documentation master file, created by
   sphinx-quickstart on Sat Feb 25 20:41:55 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Imagination
===========

:Copyright: Juti Noppornpitak <juti_n@yahoo.co.jp>
:Author:    Juti Noppornpitak <juti_n@yahoo.co.jp>
:License:   MIT

**Imagination** is a reusable component framework whose objectives are:

* encapsulates an object into a single object with the lazy loader, inspired by
  many frameworks (e.g., Symfony Framework in PHP and Spring Framework in Java),
* improves code maintainability by encapsulating reusable components (or
  dependencies) in a global memory, inspired by JavaBeans,
* introduce the concept of the aspect-oriented programming (AOP), inspired by AspectJ.

Want to get started? Please read :doc:`getting_started`.

.. note::

    Imagination plays the big role in Tori Web Framework (http://shiroyuki.com/work/project-tori)
    dealing with clean routing and globally referencing to any defined reusable components.

How to Install
--------------

Python 3.3

Releases
--------

*Development Version*

* Support Python 3.3
* Add a point cut

*Version 1.5*

* Added support for aspect-oriented programming and introduced some backward incompatibility.

*Version 1.0*

* Simple object collection repository

Reference
---------

.. toctree::
   :maxdepth: 2
   :glob:

   getting_started
   api/*

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
..
