Register a new entity with parameters
#####################################

Now, since we have one entity. Let's spice things up with more complicate
entity by creating a ``Report`` class at ``app/report.py``:

.. code-block:: python

    class Report(object):
        def __init__(self,
                     calculator,
                     assignment_scores:list,
                     final_exam_score:int):
            self.calculator        = calculator
            self.assignment_scores = assignment_scores  # max score = 10
            self.final_exam_score  = final_exam_score   # max score = 100

        def grade(self):
            total_scores     = sum(self.assignment_scores)
            total_max_scores = (10 * len(self.assignment_scores))
            assignment_part  = total_scores / total_max_scores
            final_exam_part  = final_exam_score / 100

            grade_ratio = self.calculator.add(
                assignment_part * 0.7,
                final_exam_part * 0.3
            )

            return grade_ratio * 100

At this point, again, Imagination does not know about the report. To do so,
let's register an entity of an instance of `app.report.Report` in ``containers.xml``:

.. code-block:: xml

    <imagination>
        <!-- ... (omitted) ... -->
        <entity id="report.bob" class="app.report.Report">

            <!-- Pass [2, 0, 1, 8, 6, 9, 7, 5] (list of integers)
                 as "assignment_scores" -->
            <param type="list" name="assignment_scores">
                <item type="int">2</item>
                <item type="int">0</item>
                <item type="int">1</item>
                <item type="int">8</item>
                <item type="int">6</item>
                <item type="int">9</item>
                <item type="int">7</item>
                <item type="int">5</item>
            </param>

            <!-- Pass 89 (integer)
                 as "final_exam_score" -->
            <param type="int" name="final_exam_score">89</param>

            <!-- Pass the reference of the "calc" entity
                 as "calculator" -->
            <param type="entity" name="calculator">calc</param>
        </entity>
    </imagination>

where **report.bob** is the entity ID.

.. note::

    In case you are confused, here is the equivalent code.

    .. code-block:: python

        # From the previous page...
        from app.util import Calculator

        calc = Calculator()

        # Now, to work with the report class.
        from app.report import Report

        report = Report(calc, [2, 0, 1, 8, 6, 9, 7, 5], 89)

    The key differences at this point are:

    * neither the **calc** entity and the **report.bob** entity are not
      instantiated immediately until the **report.bob** entity is requested/activated,
    * the **calc** is always activated before the **report.bob** entity as **calc**
      is a dependency of **report.bob**.
    * the objects are still living only in the scope of the container.

How to work with the report entity
==================================

To refer the report entity, for example, in ``main.py``, simply use
``report_bob = assembler.core.get('report.bob')``

Now, to actually use the entity, let's add something to the end of ``main.py``.

.. code-block:: python

    # Omitted the code for main.py already shown above
    report_bob = assembler.core.get('report.bob')
    print(report_bob.grade())  # STDOUT: 59.94999...

So, as you can see, the entity works pretty much like a normal object, except
**the key differences mentioned earlier**.

What can you define as parameters or items?
===========================================

========= ========================================== ============================
Type Name Data Type                                  Example PCDATA, child nodes
========= ========================================== ============================
str       Unicode (default)                          ``bamboo``
bool      Boolean (bool) [#pt1]_                     ``true``, ``false``
float     Float (float)                              ``1.2``, ``2.0``
int       Integer (int)                              ``123``
class     Class reference [#pt2]_                    ``argparser.ArgumentParser``
entity    **An Imagination entity** [#pt3]_          ``report.bob`` (Entity ID)
list      Python's List (list)                       (See an example below)
dict      Python's Dictionary (dict)                 (See an example below)
========= ========================================== ============================

Here is an example. From:

.. code-block:: xml

    <imagination>
        <entity class="foo.Bar" id="panda">
            <param type="bool" name="enabled">false</param>
            <param type="dict" name="data">
                <item type="list" name="collection">
                    <item type="str">shiroyuki</item>
                    <item type="str">is</item>
                    <item type="str">happy</item>
                </item>
                <item type="str" name="code">1234</item>
            </param>
        </entity>
    </imagination>

The equivalence to the Python code used to instantiate this entity will be:

.. code-block:: python

    panda = foo.Bar(enabled = False, data = {
            'collection': ['shiroyuki', 'is', 'happy'],
            'code': 1234,
        })

.. note::

    How to define parameters and items can be used with a factorized entity,
    which will be mentioned in the next step.

.. tip::

    For more information about the DTD of the configuration file, please check
    out `the DTD <https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd>`_
    on GitHub.

.. rubric:: Footnotes

.. [#pt1] Only any variations (letter case) of the word 'true' or 'false' are
          considered as a valid boolean value.
.. [#pt2] An import path of a class, as known as a fully-qualified class name,
          e.g., `argparser.ArgumentParser`
.. [#pt3] Any Imagination entity (see :doc:`../definitions`)

Next step? :doc:`05-factorization`.
