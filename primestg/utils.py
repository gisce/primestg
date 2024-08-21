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
    1: 'Arranque registrador con perdida de datos',
    2: 'Arranque registrador sin perdida de datos',
    3: 'Fallo alimentación registrador (apagado)',
    4: 'Fallo tensión de media fase 1',
    5: 'Fallo tensión de media fase 2',
    6: 'Fallo tensión de media fase 3',
    7: 'Pérdida de neutro',
    8: 'Batería baja',
    9: 'Error interno crítico ',

    11: 'Error interno crítico',
    12: 'Error de memoria de programa',
    13: 'Error de memoria RAM',
    14: 'Error de memoria NV',
    15: 'Error de Watchdog',
    16: 'Error de sistema de medidas',

    21: 'Fin Fallo tensión Fase 1',
    22: 'Fin Fallo tensión Fase 2',
    23: 'Fin Fallo tensión Fase 3',
    24: 'Cambio oficial hora: Invierno -> Verano',
    25: 'Cambio oficial hora: Verano -> Inverno',

    26: 'Habilitado led/leds impulsos marcha en vacío a ON por pulsador',
    27: 'Habilitado led/leds impulsos marcha en vacío a OFF por pulsador',
    28: 'Habilitado led/leds impulsos marcha en vacío a ON remotamente',
    29: 'Habilitado led/leds impulsos marcha en vacío a OFF remotamente',

    30: 'Cambio parámetros registrador (parámetros no incluidos en otros eventos de cambio de parámetros)',
    31: 'Cambio de configuración puertos comunicaciones',
    32: 'Cambio clave Consulta/Lectura',
    33: 'Cambio clave de Parametrización',
    34: 'Cambio clave Firmware',
    35: 'Realizado Reset de Batería',
    36: 'Cambio de Cambio Automático I/V',
    37: 'Cambio Tiempo Integración Curvas de Carga',
    38: 'Cambio Periodo Integración Curvas de Carga',
    39: 'Cambio Relación Transformación (solo para MI)',
    40: 'Cambio Tipo Sincronismo Reloj',
    41: 'Cambio Etiqueta Programación',
    42: 'Cambio Estado Activación Cierres por Pulsador',
    43: 'Cambio Asignación de Salidas',
    44: 'Cierre Contrato 1 por comando',
    45: 'Cambio parámetros Contrato 1',

    47: 'Cambio Tabla Días Especiales Contrato 1 latente',
    48: 'Cambio Tabla Temporadas Contrato 1 latente',
    49: 'Borrada Programación Contrato 1 latente',
    50: 'Cambio Cierres Automáticos Contrato 1 latente',
    51: 'Cambio Fecha Activación Contrato 1 latente',

    52: 'Cierre Contrato 2 por comando',
    53: 'Cambio parámetros Contrato 2',
    54: 'Cambio Tabla Días Especiales Contrato 2 latente',
    55: 'Cambio Tabla Temporadas Contrato 2 latente',
    56: 'Borrada Programación Contrato 2 latente',
    57: 'Cambio Cierres Automáticos Contrato 2 latente',
    58: 'Cambio Fecha Activación Contrato 2 latente',

    59: 'Cierre Contrato 3 por comando',
    60: 'Cambio parámetros Contrato 3',
    61: 'Cambio Tabla Días Especiales Contrato 3 latente',
    62: 'Cambio Tabla Temporadas Contrato 3 latente',
    63: 'Borrada Programación Contrato 3 latente',
    64: 'Cambio Cierres Automáticos Contrato 3 latente',
    65: 'Cambio Fecha Activación Contrato 3 latente',

    66: 'Cierre manual Contrato 1,2,3 (por pulsador)',

    67: 'Fin pérdida de neutro',

    90: 'Cambio de tiempo para variación de tensión (T)',
    91: 'Cambio de tiempo por interrupción larga(T\')',
    92: 'Cambio de Tensión Referencia (V)',
    93: 'Cambio de Consigna superior de tensión (+V)',
    94: 'Cambio de Consigna inferior de tensión (-V)',
    95: 'Cambio del umbral para estado de falta de tensión ',

    96: 'Activación/Cambio de Potencias contratas para la Gestión de la Potencia demandada en IMPORTACIÓN -Contrato 1 (valores anterior y nuevos)',
    97: 'Cambio de Firmware (versión anterior + versión nueva',
    98: 'Cambio hora registrador (hora anterior + hora nueva)',
    99: 'Reset de claves',
    100: 'Reset de datos',
    101: 'Reset de Parámetros',
    102: 'Activación/Cambio de Poténcias Contratas para la Gestión de la Potencia demandada en EXPORACIÓN -Contrato 3 (valores anterior y nuevos)',
    103: 'Alcance máximo número actualizaciones de software',

    104: 'Cambio del umbral de variación para considerar fraude en el neutro',
    105: 'Cambio del umbral de tiempo para considerar fraude en el neutro',
    106: 'Cambio del umbral de tiempo para la pérdida de neutro',
    107: 'Cambio del umbral (% por encima de Vref) para la pérdida de neutro',
    108: 'Cambio de scroll',

    110: 'Cambio V1 - Límite LV para eventos de caída de tensión',
    111: 'Cambio V2: límite de BT para eventos de caída de tensión y caída fuerte',
    112: 'Cambio V1 - Límite LV para eventos de aumento de tensión',
    113: 'Cambio V2 - Límite LV para eventos de aumento de tensión y aumento fuerte',
    114: 'Cambiar el umbral de tiempo para eventos de bajada de tensión LV',
    115: 'Cambiar el umbral de tiempo para eventos de aumento de tensión LV',
    116: 'Cambiar el umbral de tiempo para eventos de caída fuerte de tensión LV',
    117: 'Cambiar el umbral de tiempo para eventos de aumento fuerte de tensión LV',
    118: 'Cambio V1 - LímiteMv para eventos de caída de tensión',
    119: 'Cambio V2 - LímiteMv para eventos de caída de tensión y caída fuerte',
    120: 'Cambio V1 - LímiteMv para eventos de aumento de tensión',
    121: 'Cambio V2 - LímiteMv para eventos de aumento de tensión y aumento fuerte',
    122: 'Cambiar el umbral de tiempo  para eventos de caída de tensión MV',
    123: 'Cambiar el umbral de tiempo  para eventos de aumento de tensión MV',
    124: 'Cambiar el umbral de tiempo  para eventos de caída fuerte de tensión MV',
    125: 'Cambiar el umbral de tiempo  para eventos de aumento fuerte de tensión MV',
    126: 'Cambio del umbral de tiempo para fallos cortos y largos  de tensión (T\')',
    127: 'Tensión nominal LV cambiada',
    128: 'Tensión nominal MV cambiada',
    129: 'Umbral de tiempo para evento de corriente sobre-neutral',
    130: 'Umbral actual para eventos de corriente sobre-neutral',
    131: 'Umbral de tiempo para eventos sobrecargados (todas las fases)',
    132: 'Umbral actual para eventos sobrecargados (todas las fases)',
    133: 'Umbral de tiempo para eventos de carga desbalanceados',
    134: 'Porcentaje del umbral actual para eventos de carga desbalanceados',
    135: 'Umbral de tiempo para eventos de pérdida neutral',
    136: 'Umbral actual neutra para eventos de pérdida neutral',
    137: 'Umbral de tensión componentes secuencia zero (Vo) para eventos de pérdida neutral',
    138: 'Umbral de tensión componentes secuencia negativa (V2) para eventos de pérdida neutral',
    139: 'Umbral de tiempo para cualquier evento de pérdida de fase',
    140: 'Umbral actual neutro para cualquier evento de pérdida de fase',
    141: 'Umbral de tensión componentes secuencia zero (Vo) para cualquier evento de pérdida de fase',
    142: 'Umbral de tensíon componente secuencia negativa (V2) para cualquier evento de pérdida de fase',
    143: 'Umbral de tiempo para cualquier evento de pérdida de fase - MV',
    144: 'Umbral actual para cualquier evento de pérdida de fase - MV',
    145: 'Umbral actual fuerte para cualquier evento de pérdida de fase - MV',
    146: 'Fase DBC 1',
    147: 'Fase DBC 2',
    148: 'Fase DBC 3',
    149: 'Umbral actual para el evento DBC fase 1',
    150: 'Umbral actual para el evento DBC fase 2',
    151: 'Umbral actual para el evento DBC fase 3',
    152: 'Umbral actual mínimo para el evento DBC fase 1',
    153: 'Umbral actual mínimo para el evento DBC fase 2',
    154: 'Umbral actual mínimo para el evento DBC fase 3',

    201: 'Entrada de alarma - Inicio L01',
    202: 'Entrada de alarma - Inicio L02',
    203: 'Entrada de alarma - Inicio L03',
    204: 'Entrada de alarma - Inicio L04',
    205: 'Entrada de alarma - Inicio L05',
    206: 'Entrada de alarma - Final L01',
    207: 'Entrada de alarma - Final L02',
    208: 'Entrada de alarma - Final L03',
    209: 'Entrada de alarma - Final L04',
    210: 'Entrada de alarma - Final L05',


}, 2: {
    1: 'Conexión manual (botón)',
    2: 'Desconexión remote (comando)',
    3: 'Conexión remota (comando)',
    4: 'Desconexión por control de potencia contratada Contrato 1',
    5: 'Conexión control de potencia (IGA)',
    6: 'Inicio bloqueo elemento por superación PSC (válido para importación y exportación)',
    7: 'Habilitación del elemento',
    8: 'Deshabilitación del elemento',
    9: 'Desconexión por control de potencia residual',
    10: 'Conexión por desactivación potencia residual',
    11: 'Conexión por control de potenciaa residual',
    12: 'Cambio de modo de control del elemento de corte',
    13: 'Desconexión por control de potencia contratada Contrato 3',
    14: 'Fin bloqueo elemento por superación PSC (válido para importación y exportación',
    15: 'Desconexión por exceso de tensión o pérdida de neutro / disparo automático',
    16: 'Conexión por normalización de tensión o recuperación de neutro / reposición autónoma'
}, 3: {
    1: 'Valor medio de las tensiones entre fases bajo límite inferior',
    2: 'Tensión fase 1 bajo límite inferior',
    3: 'Tensión fase 2 bajo límite inferior',
    4: 'Tensión fase 3 bajo límite inferior',
    5: 'Valor medio de las tensiones entre fases sobre límite superior',
    6: 'Tensión fase 1 sobre límite superior',
    7: 'Tensión fase 2 sobre límite superior',
    8: 'Tensión fase 3 sobre límite superior',
    9: 'Corte de larga duración en todas las fase',
    10: 'Corte de larga duración en la fase 1',
    11: 'Corte de larga duración en la fase 2',
    12: 'Corte de larga duración en la fase 3',
    13: 'Valor medio de las tensiones entre fases de bajo límite inferior',
    14: 'Tensión fase 1 bajo límite inferior',
    15: 'Tensión fase 2 bajo límite inferior',
    16: 'Tensión fase 3 bajo límite inferior',
    17: 'Valor medio de las tensiones entre fases sobre límite superior',
    18: 'Tensión fase 1 sobre límite superior',
    19: 'Tensión fase 2 sobre límite superior',
    20: 'Tensión fase 3 sobre límite superior',
    21: 'Corte de larga duración en todas las fases',
    22: 'Corte de larga duración en la fase 1',
    23: 'Corte de larga duración en la fase 2',
    24: 'Corte de larga duración en la fase 3',
    25: 'Falta alta impedancia (Supervisor BT)',
    26: 'Fin de falta de alta impedancia (Supervisor BT)',

    201: 'Caída tensión L1 - LV',
    202: 'Caída tensión L2 - LV',
    203: 'Caída tensión L3 - LV',
    204: 'Augmento tensión L1 - LV',
    205: 'Augmento tensión L2 - LV',
    206: 'Augmento tensión L3 - LV',
    207: 'Caída fuerte de tensión L1 - LV',
    208: 'Caída fuerte de tensión L2 - LV',
    209: 'Caída fuerte de tensión L3 - LV',
    210: 'Aumento fuerte de tensión L1 - LV',
    211: 'Aumento fuerte de tensión L2 - LV',
    212: 'Aumento fuerte de tensión L3 - LV',
    213: 'Fallo corto de potencia en todas las fases',
    214: 'Fallo corto de potencia en L1',
    215: 'Fallo corto de potencia en L2',
    216: 'Fallo corto de potencia en L3',
    217: 'Caída tensión L1 - MV',
    218: 'Caída tensión L2 - MV',
    219: 'Caída tensión L3 - MV',
    220: 'Aumento tensión L1 - MV',
    221: 'Aumento tensión L2 - MV',
    222: 'Aumento tensión L3 - MV',
    223: 'Caída fuerte de tensión L1 - MV',
    224: 'Caída fuerte de tensión L2 - MV',
    225: 'Caída fuerte de tensión L3 - MV',
    226: 'Aumento fuerte de tensión L1 - MV',
    227: 'Aumento fuerte de tensión L2 - MV',
    228: 'Aumento fuerte de tensión L3 - MV',
    229: 'Pérdida neutral bajo condiciones especiales',
    230: 'Pérdida fase L1 bajo condiciones especiales',
    231: 'Pérdida fase L2 bajo condiciones especiales',
    232: 'Pérdida fase L3 bajo condiciones especiales',
    233: 'Sobrecarga fase L1',
    234: 'Sobrecarga fase L2',
    235: 'Sobrecarga fase L3',
    236: 'Sobrecorriente neutra',
    237: 'Cargas desbalanceadas bajo condiciones especiales',
    238: 'Componente secuencia zero (Vo) sobretensión',
    239: 'Componente secuencia negativa (V2) sobretensión',
    240: 'Fase DBC 1',
    241: 'Fase DBC 2',
    242: 'Fase DBC 3',
    243: 'Sobretensión de neutro respecto a la protección de tierra',
}, 4: {
    1: 'Apertura del precinto de fabricante',
    2: 'Cierre del precinto de fabricante',
    3: 'Aparición de un campo magnético superior al normal (no aplica)',
    4: 'Desaparición de un campo magnético (no aplica)',
    5: 'Presencia intensidad ante ausencia de tensión',
    6: 'Intento de acceso con clave errónea (intrusión)',
    7: 'Apertura de laa tapa cubre bornes',
    8: 'Cierre de la tapa cubre bornes',
    9: 'Inicio Detección Tensión en bornes salida ante apertura E.Corte por comando',
    10: 'Fin Detección Tensión en bornes salida ante apertura E.Corte por comando',
    11: 'Inicio Detección Impedancia infinita en bornes salida ante apertura E.Corte por comando',
    12: 'Fin Detección Impedancia infinita en bornes salida ante apertura E.Corte por comando',
    13: 'Inicio Puente Contador (opcional)',
    14: 'Fin Puente Contador (opcional)',
}, 5: {
    1: 'Recepción orden gestión de la demanda potencia residual no crítica',
    2: 'Recepción orden gestión de la demanda reducción % potencia crítica',
    3: 'Recepción orden gestión de la demanda reducción % potencia no crítica',
    4: 'Aceptación de gestión de la demanda valor absoluto no crítica',
    5: 'Aceptación de gestión de la demanda por cliente potencia residual no crítica',
    6: 'Rechazo gestión de la demanda potencia residual no crítica',
    7: 'Recepción orden gestión de la demanda reducción % potencia no crítica',
    8: 'Recepción orden gestión de la demanda por cliente reducción % potencia crítica',
    9: 'Aceptación gestión de la demanda valor absoluto potencia crítica',
    10: 'Rechazo gestión de la demanda potencia absoluta no crítica',
    11: 'Cambio valor programado potencia residual contratada. Valor previo y actual',
    12: 'Activación/Inicio reducción % potencia contratada',
    13: 'Activación/Inicio reducción % potencia absoluta',
    14: 'Fin reducción % potencia contratada',
    15: 'Fin reducción % potencia absoluta',
    16: 'Fin reducción potencia absoluta',
    17: 'Potencia demandada cercana a la potencia contratada (%)',
    18: 'Inicio establecimiento de comunicaciones puerto PLC',
    19: 'Fin de comunicaciones puerto PLC',
    20: 'Inicio establecimiento de comunicaciones puerto óptico',
}, 6: {
    1: 'Inicio establecimiento de comunicaciones puerto PLC',
    2: 'Fin de comunicaciones puerto PLC',
    3: 'Inicio establecimiento de comunicaciones puerto óptico',
    4: 'Fin de comunicaciones puerto óptico',
    5: 'Inicio establecimiento de comunicaciones puerto serie',
    6: 'Fin de comunicaciones puerto serie',
}, 7: {
    1: 'Key Reset',
    2: 'Cambio Master key',
    3: 'Cambio Global Unicast Encryption Key',
    4: 'Cambio Authentication Key',
    5: 'Cambio password LLS del cliente seguro PLC',
    6: 'Cambio Security policy (Value = 3)',
    7: 'Error cambio Master key',
    8: 'Error cambio Global Unicast Encryption Key',
    9: 'Error cambio Authentication Key',
    10: 'Error en el establecimiento de la asociación con clave dedicada',
    11: 'Error en el cifrado y autenticación de los mensajes',
    12: 'Error en el password LLS',
    13: 'Error en el cambio de Security policy',
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