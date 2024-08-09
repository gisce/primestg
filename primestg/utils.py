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
    (2, 'Grupo 2 - ICP'),
    (3, 'Grupo 3 - Calidad'),
    (4, 'Grupo 4 - Fraude'),
    (5, 'Grupo 5 - Gestión de la demanda'),
    (6, 'Grupo 6 - Alta ocurrencia'),
    (7, 'Grupo 7 - Seguridad'),
    (8, 'Grupo 8 - Fugas a tierra'),
    (9, 'Grupo 9 - Calidad de suministro')
]

# meter events
meter_event_groups = [
    (1, 'Grupo 1 - Estándar'),
    (2, 'Grupo 2 - ICP'),
    (3, 'Grupo 3 - Calidad'),
    (4, 'Grupo 4 - Fraude'),
    (5, 'Grupo 5 - Gestión de la demanda'),
    (6, 'Grupo 6 - Alta ocurrencia'),
    (7, 'Grupo 7 - Seguridad'),
]

# cnc events
cnc_event_group = [
    (1, 'Grupo 1 - Estándar'),
    (2, 'Grupo 2 - Acceso'),
    (3, 'Grupo 3 - Gestión de la demanda'),
    (4, 'Grupo 4 - Alta ocurrencia'),
    (5, 'Grupo 5 - Altas y bajas'),
    (6, 'Grupo 6 - Otros'),
]

meter_events = {1: {
    1: 'Reboot with loss of data',
    2: 'Reboot without loss of data',
    3: 'Power Fail',
    4: 'Power failure. Phase 1',
    5: 'Power failure. Phase 2',
    6: 'Power failure. Phase 3',
    7: 'Neutral loss',
    8: 'Low Battery',
    9: 'Critical Internal Error ',

    21: 'End of power failure. Phase 1',
    22: 'End of power failure. Phase 2',
    23: 'End of power failure. Phase 3',
    24: 'Official change local time Winter->Summer',
    25: 'Official change local time Summer-> Winter',
    30: 'Register parameters change',
    31: 'Communication ports parameters change',
    32: 'Reading password change',
    33: 'Parametrization password change',
    34: 'Firmware password change',
    35: 'Battery cleared',
    36: 'Automatic daylight-saving time change',
    37: 'Minimum time between billing end change',
    38: 'Load profile capture period change',
    39: 'Transform ratio changed',
    40: 'Clock synchronization mode changed',
    41: 'Program label changed',
    42: 'Manual closures activation status changed',
    43: 'Output magnitude changed',
    44: 'Closure command prompted contract 1',
    45: 'Parameters contract 1 changed',

    47: 'Special days table contract 1 passive change',
    48: 'Seasons table contract 1 passive change',
    49: 'Contract 1 passive cleared',
    50: 'Automatic billing end contract 1 passive change',
    51: 'Activation date contract 1 passive change',

    52: 'Closure command prompted contract 2',
    53: 'Parameters contract 2 changed',
    54: 'Special days table contract 2 passive change',
    55: 'Seasons table contract 2 passive change',
    56: 'Contract 2 passive cleared',
    57: 'Automatic billing end contract 2 passive change',
    58: 'Activation date contract 2 passive change',

    59: 'Closure command prompted contract 3',
    60: 'Parameters contract 3 changed',
    61: 'Special days table contract 3 passive change',
    62: 'Seasons table contract 3 passive change',
    63: 'Contract 3 passive cleared',
    64: 'Automatic billing end contract 3 passive change',
    65: 'Activation date contract 3 passive change',

    66: 'Contract 1, 2 and 3. Manual billing end (button)',

    90: 'Time threshold for voltage sags and swells changed',
    91: 'Time threshold for long power failures (T\') changed',
    92: 'Nominal voltage (Vn) changed',
    93: 'Max voltage level changed (+V)',
    94: 'Min voltage level changed (-V)',
    95: 'Difference between min voltage and no voltage changed',

    96: 'Contract Powers for Import Demand activated (new and former values)',
    97: 'Firmware changed',
    98: 'Clock synchronization',
    99: 'Passwords Reset. Passwords take the manufacturing values',
    100: 'Parameters & registers Reset. Parameters take manufacturing values and billing and load profiles values come '
         'to zero.',
    101: 'Parameters Reset',
    102: 'Contract Powers for export demand activated (new and former values)',
}, 2: {
    1: 'Manual Power control connection from meter push bottom.',
    2: 'Remote disconnection (command)',
    3: 'Remote connection (command)',
    4: 'Power contract control disconnection',
    5: 'Manual Power control connection from the household main interrupter.',
    6: 'Start of non-trip Current (valid for import and export) exceeded by blockade',
    7: 'Disconnect enabled',
    8: 'Disconnect disabled',
    9: 'Residual power control disconnection',
    10: 'Residual power deactivation control connection',
    11: 'Residual power control connection',
    12: 'Disconnect control mode changedn',
    13: 'Export Power Contract control disconnection',
    14: 'End of non-trip Current (valid for import and export) exceeded by blockade',
}, 3: {
    1: 'Quality non finished Events. Under limit voltage between phases average',
    2: 'Quality non finished Events. Under limit voltage L1',
    3: 'Quality non finished Events. Under limit voltage L2',
    4: 'Quality non finished Events. Under limit voltage L3',
    5: 'Quality non finished Events. Over limit voltage between phases average',
    6: 'Quality non finished Events. Over limit voltage L1',
    7: 'Quality non finished Events. Over limit voltage L2',
    8: 'Quality non finished Events. Over limit voltage L3',
    9: 'Quality non finished Events. Long power failure for all phases',
    10: 'Quality non finished Events. Long power failure L1',
    11: 'Quality non finished Events. Long power failure L2',
    12: 'Quality non finished Events. Long power failure L3',

    13: 'Quality finished Events. Under limit voltage between phases average',
    14: 'Quality finished Events. Under limit voltage L1',
    15: 'Quality finished Events. Under limit voltage L2',
    16: 'Quality finished Events. Under limit voltage L3',
    17: 'Quality finished Events. Over limit voltage between phases average',
    18: 'Quality finished Events. Over limit voltage L1',
    19: 'Quality finished Events. Over limit voltage L2',
    20: 'Quality finished Events. Over limit voltage L3',
    21: 'Quality finished Events. Long power failure for all phases',
    22: 'Quality finished Events. Long power failure L1',
    23: 'Quality finished Events. Long power failure L2',
    24: 'Quality finished Events. Long power failure L3',
    25: 'Missing high impedance (LVS)',
    26: 'End of missing high impedance (LVS)',
}, 4: {
    1: 'Fraud, Cover opened',
    2: 'Fraud, Cover closed',
    3: 'Fraud, Strong DC field detected',
    4: 'Fraud, No strong DC field anymore',
    5: 'Fraud, Current without voltage',
    6: 'Fraud, Communication Fraud detection',
    7: 'Terminal cover opened',
    8: 'Terminal cover closed',
    9: 'Voltage detection at output main terminals (when disconnector is opened by command)',
    10: 'End of voltage detection at output main terminals (when disconnector is opened by command)',
    11: 'High impedance detection at output main terminals (when disconnector is opened by command)',
    12: 'End of high impedance detection at output main terminals (when disconnector is opened by command)',
}, 5: {
    1: 'Reception order management critic residual demand',
    2: 'Reception order management critic % decrease demand',
    3: 'Reception order management demand absolute value critic demand',
    4: 'Reception order management no critic residual demand',
    5: 'Client acceptance management no critic residual demand',
    6: 'Client rejection management no critic residual demand',
    7: 'Reception order management no critic demand % decrease',
    8: 'Client acceptance management no critic demand % decrease',
    9: 'Rejection management no critic demand % decrease',
    10: 'Reception order management no critic absolute demand',
    11: 'Client acceptance management no critic absolute demand',
    12: 'Client Rejection management no critic absolute demand',
    13: 'subscribed residual demand changed',
    14: 'begin residual demand',
    15: 'End residual demand',
    16: 'begin decrease % subscribed demand',
    17: 'End decrease % subscribed demand',
    18: 'Begin reduction absolute power',
    19: 'End reduction absolute power',
    20: 'Demand close to Contract Power'
}, 6: {
    1: 'Frequent occurrence-common: Begin communication PLC Port',
    2: 'Frequent occurrence-common: End communication PLC Port',
    3: 'Frequent occurrence-common: Begin communication Optical Port',
    4: 'Frequent occurrence-common: End communication Optical Port',
    5: 'Frequent occurrence-common: Begin communication Serial Port',
    6: 'Frequent occurrence-common: End communications Serial Port'
}}

dc_events = {1: {
    1: 'Arranque alimentación alterna CD',
    2: 'Arranque alimentación contínua CD(si la tuviera)',
    5: 'Fallo alimentacion alterna CD',
    6: 'Fallo alimentación contínua CD(si la tuviese)',
    7: 'Batería baja',
    8: 'Cambio hora CD menor o igual de 30 segundos(NTPMaxDeviation)',
    9: 'Cambio hora CD mayor que 30 segundos (NTPMaxDeviation)',
    10: 'Error de memoria de programa',
    11: 'Error memoria RAM',
    12: 'Error memoria NV',
    13: 'Error de Watchdog',
    14: 'Error del sistema de archivos',
    15: 'Espacio libre de la memoria flash bajo (capacidad mínima libre superada)',
    16: 'Copia de seguridad realizada',
    17: 'Error de fallo del display (si lo tuviera)',
    18: 'Reserva para usos futuros. Error 01-16',
    19: 'Cambio configuración CD (parámetros)',
    20: 'Cambio configuracion puertos comunicaciones',
    21: 'Cambio Clave Consulta/Lectura, indicar usuario y método acceso',
    22: 'Cambio Clave Parametrización, indicar usuario y método acceso',
    23: 'Cambio Clave Firmware, indicar usuario y método acceso',
    24: 'Realizado Reset de Bateria, indicar usuario y método acceso',
    25: 'Realizado borrado manual de datos de medida',
    26: 'Realizado borrado automático de datos antiguos de la BD',
    27: 'Actualización de versión firmware CD',
    28: 'Actualización de versión firmware PLC PRIME (si afecta la actualización a la versión PRIME)',
    29: 'Actualización de versión firmware GPRS',
    30: 'Cambio Tipo Sincronismo Reloj',
    31: 'Cambio Asignacion de Salidas (cuando las tenga)',
    32: 'Fallo Descarga fichero firmware contador ftp desde el STG tras reintentos',
    33: 'Fallo Descarga fichero firmware concentrador ftp desde el STG tras reintentos',
    34: 'Fallo proceso actualizacion firmware contador',
    35: 'Fallo proceso actualización firmware concentrador',
    36: 'Petición errónea del STG (mensaje malformado, fechas inconsistentes, desconocido..)',
}, 2: {
    1: 'Inicio usuarios conectados al CD (usuario y contraseña)',
    2: 'Fin usuarios conectados al CD (usuario y contraseña)',
    3: 'Intento acceso con clave errónea (intrusión - usuario y contraseña)',
    4: 'Inicio usuarios conectados al CD (usuario y contraseña)',
    5: 'Fin usuarios conectados al CD (usuario y contraseña)',
    6: 'Intento acceso con clave errónea (intrusión - usuario y contraseña)',
    7: 'Apertura tapa bajo precinto fabricante',
    8: 'Cierre tapa bajo precinto fabricante',
    9: 'Apertura tapa cubrebornas/cubrehilos',
    10: 'Cierre tapa cubrebornas/cubrehilos'
}, 3: {
    1: 'Recepción orden gestión de la demanda potencia residual crítica',
    2: 'Recepción orden gestión de la demanda reducción % potencia crítica',
    3: 'Recepción orden gestión de la demanda valor abosluto de potencia crítica',
    4: 'Recepción orden gestión de la demanda potencia residual no critica',
    5: 'Aceptación gestión de la demanda por cliente potencia residual no critica',
    6: 'Rechazo gestión de la demanda por cliente potencia residual no critica',
    7: 'Recepción orden gestión de la demanda reducción % potencia no critica',
    8: 'Aceptación gestión de la demanda por cliente reducción % potencia no critica',
    9: 'Rechazo gestión de la demanda por cliente reducción % potencia no critica',
    10: 'Recepción orden gestión de la demanda potencia valor absoluto no critica',
    11: 'Aceptación gestión de la demanda por cliente potencia absoluto no critica',
    12: 'Rechazo gestión de la demanda por cliente potencia absoluto no critica',
    13: 'Cambio valor programación potencia residual contratada. Valor previo y actual',
    14: 'Activación/Inicio potencia residual. Valor previo y actual.',
    15: 'Fin potencia residual',
    16: 'Activación/Inicio reducción % potencia contratada',
    17: 'Fin reducción % potencia contratada',
    18: 'Activación/Inicio reducción potencia absoluta',
    19: 'Fin reducción potencia absoluta',
    20: 'Petición de datos desde dispositivo de cliente',
    21: 'Inicio ciclo petición de datos al contador por gestión de la demanda',
    22: 'Inicio ciclo envío automático de datos al dispositivo del cliente',
    23: 'Cambio parámetros de gestión de la demanda',
}, 4: {
    1: 'Inicio establecimiento de comunicaciones puerto PLC',
    2: 'Fin de comunicaciones puerto PLC',
    3: 'Inico establecimiento de comunicaciones puerto ETHERNET',
    4: 'Fin de comunicaciones puerto ETHERNET',
    5: 'Inico establecimiento de comunicaciones puerto GPRS',
    6: 'Fin de comunicaciones puerto GPRS',
    7: 'Inicio establecimiento de comunicaciones puerto serie RS-485',
    8: 'Fin de comunicaciones puerto serie RS-485',
    9: 'La señal de GPRS es muy débil',
    10: 'La conexión GSM/GPRS está caída.(cuando la tenga).',
    11: 'No hay tarjeta SIM instalada',
    12: 'La tarjeta SIM está pidiendo un código PIN',
    13: 'La conexión Ethernet está caída. (cuando la tenga).',
    14: 'El chip PRIME está funcionando incorrectamente o no responde',
    15: 'No existe MAC del módem PRIME definida.',
    16: 'Fallo envio WS al STG tras reintentos',
    17: 'Fallo envio fichero FTP al STG tras reintentos. Link lost while transfer',
    18: 'Fallo envio fichero FTP al STG tras reintentos. Wrong FTP username or password',
    19: 'Fallo envio fichero FTP al STG tras reintentos. Ftp service unavailable',
}, 5: {
    1: 'Alta física de un contador. Se añade un campo con el ID único del contador dado de alta en el sistema',
    2: 'Baja de un contador (física o a petición de STG). Se añade un campo con el ID único del contador dado de baja '
       'en el sistema',
}}