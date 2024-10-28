#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal

with description('Order B07 IP FTP Generation'):

    with it('generates expected B07 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B07" Version="3.1.c">\n  ' \
                          '<Cnc Id="CIR000000000">\n    ' \
                          '<B07 IPftp="10.1.5.206"/>\n  ' \
                          '</Cnc>\n</Order>\n'

        generic_values = {
            'id_pet': '1234',
            'id_req': 'B07',
            'cnc': 'CIR000000000',
            'version': '3.1.c'
        }
        payload = {
            'IPftp': '10.1.5.206',
        }
        order = Order('B07_ip')
        order = order.create(generic_values, payload)
        expect(order).to(equal(expected_result))
