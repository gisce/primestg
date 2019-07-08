#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal

with description('Order B09 Generation'):

    with it('generates expected B09 xml'):
        expected_result = '<Order IdPet="1234" IdReq="B09" Version="3.1.c">\n  ' \
                          '<Cnc Id="CIR000000000">\n    <Cnt Id="CNT000000000">\n      ' \
                          '<B09 AutMothBill="Y" Dctcp="0.00" Idm="111111111111111111111111" ' \
                          'Ip="100" Is="100" Per="3600" ScrollDispMode="C" ScrollDispTime="7" ' \
                          'Tp="2300" Ts="2300" UcorteT="50.00" Usag="180" UsobT="7.00" ' \
                          'UsubT="7.00" Uswell="180" Ut="180" Vr="230"/>\n    ' \
                          '</Cnt>\n  </Cnc>\n</Order>\n'

        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B09',
            'cnc': 'CIR000000000',
            'cnt': 'CNT000000000'
        }
        payload = {
            'Idm': '111111111111111111111111',
            'Tp': '2300',
            'Ts': '2300',
            'Ip': '100',
            'Is': '100',
            'Clec': '',
            'Cges': '',
            'Cact': '',
            'Usag': '180',
            'Uswell': '180',
            'Per': '3600',
            'Dctcp': '0.00',
            'Vr': '230',
            'Ut': '180',
            'UsubT': '7.00',
            'UsobT': '7.00',
            'UcorteT': '50.00',
            'AutMothBill': 'Y',
            'ScrollDispMode': 'C',
            'ScrollDispTime': '7'
        }
        order = Order('B09')
        order = order.create(generic_values, payload)
        expect(order).to(equal(expected_result))
