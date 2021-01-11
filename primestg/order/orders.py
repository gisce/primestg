from libcomxml.core import XmlModel, XmlField
from collections import OrderedDict
from primestg.order.base import (OrderHeader, CntOrderHeader)
from primestg.utils import ContractTemplates, datetimetoprime
from datetime import datetime
from pytz import timezone


TZ = timezone('Europe/Madrid')

SUPPORTED_ORDERS = ['B03', 'B04', 'B09', 'B11']


def is_supported(order_code):
    return order_code in SUPPORTED_ORDERS


class B03:
    """
    The class used to instance B03 order.

    :return: B03 order with parameters
    """
    def __init__(self, generic_values, payload):
        self.generic_values = generic_values
        self.order = CntOrderHeader(
            generic_values.get('id_pet'),
            generic_values.get('id_req'),
            generic_values.get('cnc'),
            generic_values.get('cnt')
        )
        self.order.cnc.cnt.feed({'payload': B03Payload(payload)})
        # Load generic order with values


class B03Payload(XmlModel):
    """
    The class used to instance B03 parameters.
    Supported parameters:
        Fini: Execution date
        Ffin: Maximum Execution Date
        Order:
            0 -> OPEN
            1 -> CLOSE
            2 -> CLOSE/RECONNECT
    :return: B03 parameters

    """
    def __init__(self, payload, drop_empty=False):
        self.payload = XmlField(
            'B03', attributes={
                'Order': payload.get('order_param'),
                'Fini': payload.get('date_from'),
                'Ffin': payload.get('date_to'),
            })
        super(B03Payload, self).__init__('b03Payload', 'payload', drop_empty=drop_empty)


# B04 Node classes
class Contract(XmlModel):
    """
    The class to instance B04 Contract
    Parameters:
        contract: Contract number (1,2,3)
        calendar_type: Calendar type:
            '01': season
            '0A': summer/winter
        'name': 6 ascii chars calendar name i.e '2.0TDA'
        'activation_date':  Datetime of activation localized or not. It gets always CE(S)T timezone
    """
    _sort_order = ('contract', 'seasons_list', 'weeks_list', 'days_list', 'special_days_list')

    def __init__(self, payload, drop_empty=False):
        self.contract = XmlField(
            'Contract', attributes={
                'c': str(payload.get('contract')),
                'CalendarType': payload.get('calendar_type', '01'),
                'CalendarName': self.name2octet(payload.get('name')),
                'ActDate': payload.get('activation_date'),
            }
        )
        self.seasons_list = []
        self.weeks_list = []
        self.days_list = []
        self.special_days_list = []
        super(Contract, self).__init__(
            'Contract', 'contract', drop_empty=drop_empty
        )

    @staticmethod
    def name2octet(txt):
        octet_str = ''
        for caracter in '{: >6}'.format(txt):
            octet_str += '{0:2x}'.format(ord(caracter)).upper()
        return octet_str

    @staticmethod
    def octet2name(txt):
        name = ''
        for index in range(0, len(txt), 2):
            name += chr(int(txt[index] + txt[index + 1], 16))
        return name


class Season(XmlModel):
    """
    The class to instance B04 Seasons
    Parameters:
        name: Season Name i.e 01
        start_date: Datetime string with Wildcards i.e: FFFF0101FF00000000800000
        week: Week Name i.e: 01
    """
    def __init__(self, payload, drop_empty=False):
        self.season = XmlField(
            'Season', attributes={
                'Name': payload.get('name'),
                'Start': payload.get('start'),
                'Week': payload.get('week')
            }
        )
        super(Season, self).__init__('Season', 'season', drop_empty=drop_empty)

class Week(XmlModel):
    """
    The class to instance B04 Week
    Parameters:
        name: Week Name i.e 01
        week: String with 7 day names (one per day) i.e. "01010101010202"
    """
    def __init__(self, payload, drop_empty=False):
        self.week = XmlField(
            'Week', attributes={
                'Name': payload.get('name'),
                'Week': payload.get('week')
            }
        )
        super(Week, self).__init__('Week', 'week', drop_empty=drop_empty)


class SpecialDays(XmlModel):
    """
    The class to instance B04 Special Days
    Parameters:
        datetime: PRIME Datetime with wildcards, i.e: FFFF0101000000000W
        datetime_card:
            True: Year as Wildcard (Y)
            False: Year as is      (N)
        day_id: Day Id as defined in Day spec (i.e: "01")
    """
    def __init__(self, payload, drop_empty=False):
        self.specialdays = XmlField(
            'SpecialDays', attributes={
                'DT': payload.get('datetime'),
                'DTCard': payload.get('datetime_card') and 'Y' or 'N',
                'DayID': payload.get('day_id')
            }
        )
        super(SpecialDays, self).__init__('SpecialDays', 'specialdays', drop_empty=drop_empty)


class ChangeHour(XmlModel):
    """
    The class to instance B04 Period Change Hour
    Parameters:
        hour: integer (0 to 23)
        period: integer(1 to 6)
    """

    def __init__(self, payload, drop_empty=False):
        self.change_hour = XmlField(
            'Change', attributes={
                'Hour': "{0:02x}000000".format(payload.get('hour')).upper(),
                'TariffRate': "{0:04d}".format(payload.get('period'))
            }
        )
        super(ChangeHour, self).__init__('ChangeHour', 'change_hour')


class Day(XmlModel):
    """
    The class to instance B04 Day
    Parameters:
        id: day id i.e 01
        days: ChangeHour class list
    """

    _sort_order = ('day', 'change_hour_list')

    def __init__(self, payload, drop_empty=False):
        self.day = XmlField(
            'Day', attributes={'id': payload.get('id')}
        )
        self.change_hour_list = []
        super(Day, self).__init__('Day', 'day', drop_empty=drop_empty)


class B04:
    """
    The class used to instance B04 order.

    :return: B04 order with parameters
    """
    def __init__(self, generic_values, payload):
        self.generic_values = generic_values
        self.order = CntOrderHeader(
            generic_values.get('id_pet'),
            generic_values.get('id_req'),
            generic_values.get('cnc'),
            generic_values.get('cnt')
        )
        self.order.cnc.cnt.feed({'payload': B04Payload(payload)})
        # Load generic order with values


class B04Payload(XmlModel):
    """
    The class used to instance B04 parameters.
    Supported parameters:
        contract: One of available contracts (1,2,3)
        template: Name of one of available templates
        activation_date: Activation date if latent. Admits wildcards: YYYYMMDDHH (FFFF0101FF)

    :return: B04 parameters

    """

    _sort_order = ('payload', 'contract',)

    def __init__(self, payload,  drop_empty=False):
        contract = payload.get('contract')
        template_name = payload.get('name')
        act_date_param = payload.get('activation_date')

        activation_date = datetimetoprime(act_date_param)

        # Get template
        ct = ContractTemplates()
        tmpl = ct.get_template(template_name)

        # Creates lists
        seasons = []
        for season in tmpl['seasons']:
            seasons.append(
                Season(season)
            )

        weeks = []
        for week in tmpl['weeks']:
            weeks.append(
                Week(week)
            )

        days = []
        for day_id in sorted(tmpl['days']):
            hours = tmpl['days'][day_id]
            chs = []
            for ch in hours:
                chs.append(ChangeHour(ch))
            day = Day({'id': day_id})
            day.feed({'change_hour_list': chs})
            days.append(day)

        special_days = []
        for sp_day in tmpl.get('special_days', []):
            special_days.append(
                SpecialDays(sp_day)
            )

        self.payload = XmlField('B04')
        self.contract = Contract(
                {'name': template_name, 'contract': contract, 'activation_date': activation_date}
            )

        self.contract.feed(
            {
                'seasons_list': seasons,
                'weeks_list': weeks,
                'days_list': days,
                'special_days_list': special_days
            }
        )

        super(B04Payload, self).__init__('b04Payload', 'payload', drop_empty=drop_empty)


class B09:
    """
    The class used to instance B09 order.

    :return: B09 order with parameters
    """
    def __init__(self, generic_values, payload):
        self.generic_values = generic_values
        self.order = CntOrderHeader(
            generic_values.get('id_pet'),
            generic_values.get('id_req'),
            generic_values.get('cnc'),
            generic_values.get('cnt')
        )
        self.order.cnc.cnt.feed({'payload': B09Payload(payload)})
        # Load generic order with values


class B09Payload(XmlModel):
    """
    The class used to instance B09 parameters.
    Supported parameters:
        Idm: Id Comunic. Multicast
        Tp: Primary voltage (supervision or T4 meters)
        Ts: Secondary voltage (supervision or T4 meters)
        Ip: Primary current (supervision or T4 meters)
        Is: Secondary current (supervision or T4 meters)
        Clec: Reading key
        Cges: Parametrization key
        Cact: Updating (firmware) key
        Usag: Time threshold for Voltage sags
        Uswell: Time threshold for Voltage swells
        Per: Load profiel Period (as DLMS capture period)
        Dctcp: Demand close contracted power.
        Vr: Reference voltage
        Ut: Long Power Failure threshold
        UsubT: Voltage sag threshold
        UsobT: Voltage sweel threshold
        UcorteT: Voltage cut-off threshold
        AutMothBill: Enable/Disable automatic monthly billing
        ScrollDispMode: Scroll Display Mode
        ScrollDispTime: Time for Scroll Display
    :return: B09 parameters

    """
    def __init__(self, payload, drop_empty=False):
        # Discard empty strings and values and compose field
        attributes = {k: v for k, v in payload.items() if v is not None and v != ""}
        self.payload = XmlField('B09', attributes=attributes)
        super(B09Payload, self).__init__('b09Payload', 'payload', drop_empty=drop_empty)


class B11:
    """
    The class used to instance B11 order.

    :return: B11 order with parameters
    """
    def __init__(self, generic_values, payload):
        self.generic_values = generic_values
        self.order = OrderHeader(
            generic_values.get('id_pet'),
            generic_values.get('id_req'),
            generic_values.get('cnc'),

        )
        self.order.cnc.feed({'payload': B11Payload(payload)})
        # Load generic order with values


class B11Payload(XmlModel):
    """
    The class used to instance B11 parameters.
    Supported parameters:
        Order:
            T01 -> Reboot of the DC
            T02 -> Stop and cancel all running reports scheduled
            T03 -> Sync meter time according to TimeDev and TimeDevOver
            T04 -> Perform a Clear of meters database in DC that are in Permanent Failure (PF) state
            T05 -> Force time synchronisation in DC
            T06 -> Clean meter passwords
            T07 -> Force meter sync ignoring parameters TimeDev and TimeDevOver
        Args: String with additional arguments when needed
        Fini: Execution date
        Ffin: Maximum Execution Date
    :return: B11 parameters
    """
    def __init__(self, payload, drop_empty=False):
        self.payload = XmlField(
            'B11', attributes={
                'Order': payload.get('txx'),
                'Args': '',
                'Fini': payload.get('date_from'),
                'Ffin': payload.get('date_to'),
            })
        super(B11Payload, self).__init__('b11Payload', 'payload', drop_empty=drop_empty)


class Order(object):
    """
    Order class
    """
    def __init__(self, order):
        """
        Creates a Order object.

        :param order_type: BXX Order Type
        :return: an Order object
        """
        self.order_type = order

    def create(self, generic_values, payload):
        """
        Prepares a XML string to send to a concentrator

        :return: Order formatted in XML
        """
        order_type_class = {
            'B03': {
                'class': B03,
                'args': [generic_values, payload]
            },
            'B04': {
                'class': B04,
                'args': [generic_values, payload]
            },
            'B09': {
                'class': B09,
                'args': [generic_values, payload]
            },
            'B11': {
                'class': B11,
                'args': [generic_values, payload]
            }
        }

        if self.order_type not in order_type_class:
            raise NotImplementedError('Order type not implemented!')

        get = order_type_class.get(self.order_type).get
        order_class = get('class')
        order_args = get('args')
        order_obj = order_class(*order_args)
        order_obj.order.build_tree()
        order_obj.order.pretty_print = True
        xml = str(order_obj.order)
        formatted_xml = xml.replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n', '')
        return formatted_xml

    @property
    def supported(self):
        return is_supported(self.order_type)
