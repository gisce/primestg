#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual

with description('Order B03 Generation'):

    with it('generates expected B03 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B03" Version="3.1.c">\n  ' \
                          '<Cnc Id="CIR000000000">\n    <Cnt Id="CNT000000000">\n      ' \
                          '<B03 Ffin="" Fini="" Order="5"/>\n    </Cnt>\n  </Cnc>\n</Order>\n'

        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B03',
            'cnc': 'CIR000000000',
            'cnt': 'CNT000000000'
        }
        payload = {
            'order_param': '5',
            'date_from': '',
            'date_to': '',
        }
        order = Order('B03')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)
