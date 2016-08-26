.. Imagination documentation master file, created by
   sphinx-quickstart on Sat Feb 25 20:41:55 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Imagination v1
==============

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

Want to see the reference for XML configuration files? Please read
:doc:`api/helper.assembler`.

.. note::

    Imagination plays the big role in Tori Web Framework
    (http://shiroyuki.com/work/project-tori) dealing with clean routing and
    globally referencing to any defined reusable components.

How to Install
--------------

:PIP:   pip install imagination
:Make:  make install
:Setup: python setup.py install

Architecture
------------

  Assembler ---> Locator --+--> Entity ---> Loader
                           |       |
                           |       +-----------------+--> InterceptableObject
                           |                         |
                           +--> Factorization -------+
                           |
                           +--> Proxy

Release Notes
-------------

*Version 1.17*

* Improve the error message when the loader handles non-existing modules or references in a target module.

*Version 1.16*

* BUGFIX: Prevent the non-callable properties from being intercepted.

*Version 1.15*

* Add the support for delayed injections when the factory service is not ready to use during the factorization. (1.10.0)
* Fix compatibility with Python 2.7, 3.3, 3.4, 3.5 and 3.6 (dev).
* Improve the stability.

*Version 1.9*

* Add a entity factorization.

*Version 1.8*

* Add a callback proxy for dynamic programming. (http://imagination.readthedocs.org/en/latest/getting_started.html#callback-proxy)

*Version 1.7*

* Fixed bugs related to data access and conversion.
* Added extra lazy loading on entity containers (delaying the
  instantiation/forking of the target entity).
* Added cross-document reference when ``imagination.helper.assembler.Assembler``
  load the configuration from multiple files (used in Tori Framework 2.2).

*Version 1.6*

* Support Python 3.3.
* Support lists and dictionaries in the XML configuration file.

*Version 1.5*

* Added support for aspect-oriented programming and introduced some backward incompatibility.

*Version 1.0*

* Simple object collection repository

MIT License
-----------

Copyright (c) 2012-2013 Juti Noppornpitak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
