from libcomxml.core import XmlModel, XmlField
from primestg.order.base import (OrderHeader, CntOrderHeader)

SUPPORTED_ORDERS = ['B03', 'B09', 'B11']


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
