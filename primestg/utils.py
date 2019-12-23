#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example


def assertXMLEqual(got, want):
    checker = LXMLOutputChecker()
    if checker.check_output(want, got, 0):
        return
    message = checker.output_difference(Example(u"", want), got, 0)
    raise AssertionError(message)

