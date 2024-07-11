# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual
from datetime import datetime

with description('Order B02 Generation'):
    with before.all:
        self.expected_result = (
            """
            <Order IdPet="1234" IdReq="B02" Version="3.1.c">   
                <Cnc Id="CIR000000000">
                    <Cnt Id="CNT000000000">
                        <B02 ActDate="{0}">
                            <Contrato1 TR1="1000" TR2="2000" TR3="3000" TR4="4000" TR5="5000" TR6="6000"/>
                        </B02>
                    </Cnt>
                </Cnc>
            </Order>
            """
        )
    with it('generates expected B02 xml'):
        generic_values = {
            'id_pet': str(1234),
            'id_req': 'B02',
            'cnc': 'CIR000000000',
            'cnt': 'CNT000000000'
        }
        payload = {
            'activation_date': datetime(2021, 4, 1),
            'powers': ['1000', '2000', '3000', '4000', '5000', '6000']
        }
        order = Order('B02')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_result.format('20210401000000000S'))
