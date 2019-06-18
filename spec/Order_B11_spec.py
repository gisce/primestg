#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal

with description('Order B11 Generation'):

    with it('generates expected B11 T05 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B11" Version="3.1.c">\n  ' \
                          '<Cnc Id="CIR4621544074">\n    <B11 Args="" ' \
                          'Ffin="" Fini="" Order="T05"/>\n  </Cnc>\n</Order>\n'

        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B11',
            'cnc': 'CIR4621544074'
        }
        payload = {
            'txx': 'T05',
            'date_from': '',
            'date_to': '',
        }

        order = Order('B11')
        order = order.create(generic_values, payload)

        expect(order).to(equal(expected_result))
