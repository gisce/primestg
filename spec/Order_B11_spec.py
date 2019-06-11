#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primestg.order.orders import B11
from expects import expect, equal

with description('Order B11 Generation'):
    with before.all:

        self.data_filenames = [
            'spec/data/B11.xml',
        ]

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
        b11 = B11(generic_values, payload)
        b11.order.build_tree()
        b11.order.pretty_print = True

        xml = str(b11.order)
        formatted_xml = xml.replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n', '')
        expect(formatted_xml).to(equal(expected_result))
