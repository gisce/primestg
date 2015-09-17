========
PrimeSTG
========

.. image:: https://travis-ci.org/gisce/primestg.png?branch=master
    :target: https://travis-ci.org/gisce/primestg
    :alt: Build status

Python library of Prime STG-DC Interface Specification

Read the documentation at http://primestg.readthedocs.org

.. code-block:: python

    from primestg.report import Report

    # xml is a basestring with a filename or a file object with the report
    report = Report(xml)

    # get all values of the report
    values = report.values

    # get the values of first concentrator
    values = report.concentrators[1].values

    # get the values of second meter of the first concentrator
    values = report.concentrators[1].meters[2].values

    # get the first value set of second meter of the first concentrator
    values = report.concentrators[1].meters[2].measures[1].values

    # get the parameters of the first concentrator from report S12
    values = report.concentrators[1].parameters[1].values
