# -*- coding: utf-8 -*-
from __future__ import absolute_import

from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example
from .contract_templates import CONTRACT_TEMPLATES
from pytz import timezone
from copy import copy

TZ = timezone('Europe/Madrid')


def assertXMLEqual(got, want):
    checker = LXMLOutputChecker()
    if checker.check_output(want, got, 0):
        return
    message = checker.output_difference(Example(u"", want), got, 0)
    raise AssertionError(message)


def datetimetoprime(dt):
    """
    Converts a datetime (localized or not) to a prime datetime string.
    """
    dt_param = copy(dt)
    if dt.tzinfo is None:
        dt_param = TZ.normalize(TZ.localize(dt_param))
    season = dt_param.dst() and 'S' or 'W'
    dt_str = dt_param.strftime(
        '%Y%m%d%H%M%S000{}'.format(season)
    )
    return dt_str


def name2octet(txt):
    octet_str = ''
    for caracter in '{: >6}'.format(txt):
        octet_str += '{0:2x}'.format(ord(caracter)).upper()
    return octet_str


def octet2name(txt):
    name = ''
    for index in range(0, len(txt), 2):
        name += chr(int(txt[index] + txt[index + 1], 16))
    return name


def octet2hour(txt):
    return int(txt[0:2], 16)


class ContractTemplates:

    def __init__(self):
        self.templates = CONTRACT_TEMPLATES

    def get_available_templates(self, origin=None):
        template_list = []
        for name, contract in self.templates.items():
            if origin is not None:
                if contract['origin'] != origin:
                    continue
            template_list.append(
                (name, contract['description'], contract['origin'])
            )
        return template_list

    def get_template(self, name):
        try:
            return self.templates[name]
        except Exception as e:
            raise KeyError('Template not available')
