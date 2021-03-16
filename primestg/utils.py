# -*- coding: utf-8 -*-
from __future__ import absolute_import

from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example
from .contract_templates import CONTRACT_TEMPLATES
from .dlms_templates import DLMS_TEMPLATES
from pytz import timezone
from copy import copy

from datetime import datetime

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


def datetohexprime(dt):
    """
    Converts a date to a hexadecimal prime date string
    """
    year = dt.year
    month = dt.month
    day = dt.day

    date_string = '{0:04x}{1:02x}{2:02x}'.format(year, month, day).upper()

    return date_string


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


def octet2number(txt):
    return int(txt, 16)


def octet2date(txt):
    year = octet2number(txt[0:4])
    month = octet2number(txt[4:6])
    day = octet2number(txt[6:8])
    hour = octet2number(txt[8:10])
    minute = octet2number(txt[10:12])
    second = octet2number(txt[12:14])

    return datetime.strptime('{}-{}-{} {}:{}:{}'.format(year, month, day, hour, minute, second), '%Y-%m-%d %H:%M:%S')


class PrimeTemplates:

    def __init__(self):
        self.templates = {}

    def get_available_templates(self, origin=None, template_type=None):
        template_list = []
        for name, contract in self.templates.items():
            if origin is not None and contract['origin'] != origin:
                continue
            if template_type is not None and contract['category'] != template_type:
                continue

            template_list.append((name, contract['description'], contract['origin']))

        return template_list

    def get_template(self, name):
        try:
            return self.templates[name]
        except Exception as e:
            raise KeyError('Template not available')


class ContractTemplates(PrimeTemplates):

    def __init__(self):
        self.templates = CONTRACT_TEMPLATES


class DLMSTemplates(PrimeTemplates):

    def __init__(self):
        self.templates = DLMS_TEMPLATES

    def generate_cycle_file(self, template_name, meters_name, params=None):
        elements = self.get_template(template_name)['data']
        if params is None:
            params = {}

        xml = '<cycles>\n<cycle name="Ciclo_{}_raw" period="1" immediate="true" repeat="1" priority="1">\n'.format(
            template_name)

        for meter_name in meters_name:
            xml += '<device sn="{}"/>\n'.format(meter_name)

        for element in elements:
            xml += '<set obis="{}" class="{}" element="{}">{}</set>\n'.format(
                element['obis'], element['class'], element['element'], element['data'].format(**params))

        xml += '</cycle>\n</cycles>'

        return xml
