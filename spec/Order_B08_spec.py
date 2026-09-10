#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual
from datetime import datetime

with description('Order B08 Generation'):

    with it('generates expected B08 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B08" Version="3.4">\n  ' \
                          '<Cnc Id="CIR000000000">\n      ' \
                          '<B08 ActDate="20260301000000000W" Firmware="/firmware/4WF01610010_cct_3_23_80_27_36371.dat"/>\n  </Cnc>\n</Order>\n'

        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B08',
            'cnc': 'CIR000000000',
            'version': '3.4',
        }
        payload = {
            'activation_date': datetime(2026,3,1,0),
            'path': '/firmware/4WF01610010_cct_3_23_80_27_36371.dat'
        }
        order = Order('B08')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)
