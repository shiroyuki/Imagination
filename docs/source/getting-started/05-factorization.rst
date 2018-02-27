Dynamically define an entity with a factory entity
##################################################

From the previous step, you probably have an idea how to define an entity with
parameters. However, the "report" example from the previous step is not really
accetptable if we have to dynamically define the report of the first place in
the school.

First, we create a service class ``ReportRepository`` at ``app/repo.py``:

.. code-block:: python

    class ReportRepository(object):
        def __init__(self, calculator):
            self.calculator = calculator

        def find_one_by_rank(self, rank):
            first_place = ... # Omit the logical code to generate
                              # a report by rank to keep this
                              # example very short.

            return first_place

Then, register this class as a normal entity in ``containers.xml``:

.. code-block:: xml

    <imagination>
        <!-- ... (refer to the previous step) ... -->
        <entity id="report.repo" class="app.repo.ReportRepository">
            <param type="entity" name="calculator">calc</param>
        </entity>
    </imagination>

Now, define an entity for the first-place report.

.. code-block:: xml

    <imagination>
        <!-- ... (refer to the previous step) ... -->
        <factorization id="report.first"
                       with="report.repo"
                       call="find_one_by_rank">
            <param type="int" name="rank">1</param>
        </factorization>
    </imagination>

Now, you have an entity called **report.first**. We call this a factorized
entity (see more at :doc:`../definitions`).

.. note::

    In this case, the entity **report.repo** is a dependency of the entity
    ``report.first``. Hence, **report.repo** will always be activated first.

How to work with the first-place report entity
==============================================

To refer the first-place report entity, for example, in ``main.py``, simply do:

.. code-block:: python

    # Omitted the code for main.py already shown above
    report_first = assembler.core.get('report.first')

.. tip::

    For more information about the DTD of the configuration file, please check
    out `the DTD <https://github.com/shiroyuki/Imagination/blob/master/imagination.dtd>`_
    on GitHub.

Next step? :doc:`06-lambda-entity`.
