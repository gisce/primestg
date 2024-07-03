========
PrimeSTG
========

.. image:: https://github.com/gisce/primestg/actions/workflows/python2.7-app.yml/badge.svg
    :target: https://github.com/gisce/primestg/actions/workflows/python2.7-app.yml
    :alt: Build status

.. image:: https://github.com/gisce/primestg/actions/workflows/python3.11-app.yml/badge.svg
    :target: https://github.com/gisce/primestg/actions/workflows/python3.11-app.yml
    :alt: Build status

Python library of Prime STG-DC Interface Specification

Read the documentation at http://primestg.readthedocs.org

How it works
============

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

Warnings property
-----------------

All reports supported by the library have a warnings property that informs of problems found while parsing the contents of it. Depending on the type of report the warnings will be structured one way or another.

**Meter information report:**

The best way to get the warnings for these reports would be asking for the warnings of every meter in it.

.. code-block:: python

    for meter in cnc.meters:                        
        if meter.warnings:
            warnings.append(meter.warnings)

These will give us a list of dictionaries where each of them will have the serial name of the meter as a key and a list of strings with every exception found while reading as a value.

**Concentrator information report:**

To obtain the warnings from a concentrator report we will use the warnings property from the concentrator object directly.

.. code-block:: python

    for cnc in self.report[key].concentrators:
        if cnc.warnings:
            warnings.append(cnc.warnings)

This give us a list of strings where each one is the message of an exception found while reading.
