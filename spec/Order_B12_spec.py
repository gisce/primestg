# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual

with description('Order B12 Generation'):

    with it('generates expected B12 Powers xml'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">   
                    <Cnc Id="CIR4621544074">
                        <Cnt Id="CNT000000000">
                            <B12 Ffin="" Fini="">
                                <set class="3" data="raw{ 06 00 00 14 1e }" element="2" obis="0.1.94.34.11.255"/>
                                <set class="3" data="raw{ 06 00 00 14 82 }" element="2" obis="0.1.94.34.12.255"/>
                                <set class="3" data="raw{ 06 00 00 14 e6 }" element="2" obis="0.1.94.34.13.255"/>
                                <set class="3" data="raw{ 06 00 00 15 4a }" element="2" obis="0.1.94.34.14.255"/>
                                <set class="3" data="raw{ 06 00 00 15 ae }" element="2" obis="0.1.94.34.15.255"/>
                                <set class="3" data="raw{ 06 00 00 16 12 }" element="2" obis="0.1.94.34.16.255"/>
                            </B12>
                        </Cnt>
                    </Cnc>
                </Order>""")

        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B12',
            'cnc': 'CIR4621544074',
            'cnt': 'CNT000000000',
        }
        payload = {
            'template': 'C1_ACT_POWERS',
            'powers': [5150, 5250, 5350, 5450, 5550, 5650],
            'date_from': '',
            'date_to': '',
        }

        order = Order('B12')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)
