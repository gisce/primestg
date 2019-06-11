from libcomxml.core import XmlModel, XmlField
from primestg.order.base import Order

SUPPORTED_ORDERS = ['B11']


def is_supported(order_code):
    return order_code in SUPPORTED_ORDERS


class B11:

    def __init__(self, generic_values, payload):
        self.generic_values = generic_values
        self.order = Order(
            generic_values.get('id_pet'),
            generic_values.get('id_req'),
            generic_values.get('cnc'),

        )
        self.order.cnc.feed({'payload':B11Payload(payload)})
        # Load generic order with values


class B11Payload(XmlModel):

    def __init__(self, payload, drop_empty=False):
        self.payload = XmlField(
            'B11', attributes={
                'Order': payload.get('txx'),
                'Args': '',
                'Fini': payload.get('date_from'),
                'Ffin': payload.get('date_to'),
            })
        super(B11Payload, self).__init__('b11Payload', 'payload', drop_empty=drop_empty)
