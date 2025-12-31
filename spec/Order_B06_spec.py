#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual

with description('Order B06 Generation'):

    with it('generates expected B06 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B06" Version="3.4">\n  ' \
                          '<Cnc Id="CIR000000000">\n    <Cnt Id="CNT000000000">\n      ' \
                          '<B06 Operation="1"/>\n    </Cnt>\n  </Cnc>\n</Order>\n'
        import pdb; pdb.set_trace()
        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B06',
            'cnc': 'CIR000000000',
            'cnt': 'CNT000000000',
            'version': '3.4',
        }
        payload = {
            'operation': '1',
        }
        order = Order('B06')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)
