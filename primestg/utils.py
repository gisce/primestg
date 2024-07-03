# -*- coding: utf-8 -*-
from __future__ import absolute_import

from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example
from .contract_templates import CONTRACT_TEMPLATES
from .dlms_templates import DLMS_TEMPLATES
from pytz import timezone
from copy import copy
from string import printable

from datetime import datetime
from dateutil.relativedelta import relativedelta

TZ = timezone('Europe/Madrid')
PRIORITY_VERYHIGH = 1
PRIORITY_HIGH = 2
PRIORITY_NORMAL = 3

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
        c = chr(int(txt[index] + txt[index + 1], 16))
        if c in printable:
            name += c
        else:
            break
    return name


def octet2number(txt):
    return int(txt, 16)


def octet2date(txt):
    hexadecimal = True
    year = octet2number(txt[0:4])
    if txt.startswith('FFFF'):
        year = 9999
        hexadecimal = False
    elif year > 3000:
        hexadecimal = False
        year = int(txt[0:4])
    elif year == 0:
        hexadecimal = False
        year = 0000
    month = hexadecimal and octet2number(txt[4:6]) or int(txt[4:6])
    if month < 1 or month > 12:
        month = 1
    day = hexadecimal and octet2number(txt[6:8]) or int(txt[6:8])
    if day < 1 or day > 31:
        day = 1
    hour_txt = txt[8:10]
    if hour_txt == 'FF':
        hour = 0
    else:
        hour = hexadecimal and octet2number(hour_txt) or int(hour_txt)
    minute_txt = txt[10:12]
    if minute_txt == 'FF':
        minute = 0
    else:
        minute = hexadecimal and octet2number(minute_txt) or int(minute_txt)
    second_txt = txt[12:14]
    if second_txt == 'FF':
        second = 0
    else:
        second = hexadecimal and octet2number(txt[12:14]) or int(second_txt)

    return datetime.strptime('{}-{}-{} {}:{}:{}'.format(year, month, day, hour, minute, second), '%Y-%m-%d %H:%M:%S')

def prepare_params(payload):
        """
        Prepares payload to DLMS format
        payload = {
            powers: list [p1, p2, p3, p4, p5, p6]
            date: datetime.date
        }
        returns params dict converted to DMLS
        {
            powers: dict {'p1': hexnumber, 'p2': hexnumber ....}
            date: hexdate

        """
        powers = payload.get('powers', ['15000', '15000', '15000', '15000', '15000', '15000'])
        latent_date = payload.get('date', (datetime.today() + relativedelta(days=1)).date())

        params = {}
        hex_powers = dict(zip(['p1', 'p2', 'p3', 'p4', 'p5', 'p6'], powers))
        for period, power in hex_powers.items():
            hexnumber = '{0:08x}'.format(int(power))
            hex_powers[period] = ''.join([hexnumber[i:i + 2] for i in range(0, 8, 2)])
        params.update(hex_powers)
        params.update({'date': datetohexprime(latent_date)})
        return params

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

    def generate_cycle_file(self, template_name, meters_name, params=None, root=True):
        cycles_xml =self.generate_cycles(template_name, meters_name, params=params)
        if root:
            return "<cycles>\n{}\n</cycles>".format(cycles_xml)
        else:
            return cycles_xml

    def generate_cycles(self, template_name, meters_name, params=None):
        elements = self.get_template(template_name)['data']
        if params is None:
            params = {}
        else:
            params = prepare_params(params)

        xml = '<cycle name="Ciclo_{}_raw" period="1" immediate="true" repeat="1" priority="1">\n'.format(
            template_name)

        for meter_name in meters_name:
            xml += '<device sn="{}"/>\n'.format(meter_name)

        for element in elements:
            xml += '<set obis="{}" class="{}" element="{}">{}</set>\n'.format(
                element['obis'], element['class'], element['element'], element['data'].format(**params))

        xml += '</cycle>'

        return xml


event_groups = [
    (1, 'Grupo 1 - Estándar'),
    (2, 'Grupo 2 - Acceso'),
    (3, 'Grupo 3 - Gestión de la demanada'),
    (4, 'Grupo 4 - Alta ocurrencia'),
    (5, 'Grupo 5 - Altas y bajas'),
    (6, 'Grupo 6 - Otros'),
    (7, 'Grupo 7 - Otros'),
    (8, 'Grupo 8 - Fugas a tierra'),
    (9, 'Grupo 9 - Calidad de suministro')
]