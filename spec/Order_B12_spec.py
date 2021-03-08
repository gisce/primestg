# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual
from datetime import date

with description('Order B12 Generation'):

    with it('generates expected B12 Latent Powers xml'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">   
                    <Cnc Id="CIR4621544074">
                        <Cnt Id="CNT000000000">
                            <B12 Ffin="" Fini="">
                                <set class="3" data="raw{060000141e}" element="2" obis="0.1.94.34.11.255"/>
                                <set class="3" data="raw{0600001482}" element="2" obis="0.1.94.34.12.255"/>
                                <set class="3" data="raw{06000014e6}" element="2" obis="0.1.94.34.13.255"/>
                                <set class="3" data="raw{060000154a}" element="2" obis="0.1.94.34.14.255"/>
                                <set class="3" data="raw{06000015ae}" element="2" obis="0.1.94.34.15.255"/>
                                <set class="3" data="raw{0600001612}" element="2" obis="0.1.94.34.16.255"/>
                                <set class="20" data="raw{090C07E50601FF000000000800FF}" element="10" obis="0.0.13.0.1.255"/>
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
            'template': 'C1_LAT_POWERS',
            'powers': [5150, 5250, 5350, 5450, 5550, 5650],
            'date': date(2021, 6, 1),
            'date_from': '',
            'date_to': '',

        }

        order = Order('B12')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)

    with it('generates expected B12 Actual Powers xml'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">
                    <Cnc Id="CIR4621544074">
                        <Cnt Id="CNT000000000">
                            <B12 Ffin="" Fini="">
                                <set class="3" data="raw{060000141e}" element="2" obis="0.1.94.34.11.255"/>
                                <set class="3" data="raw{0600001482}" element="2" obis="0.1.94.34.12.255"/>
                                <set class="3" data="raw{06000014e6}" element="2" obis="0.1.94.34.13.255"/>
                                <set class="3" data="raw{060000154a}" element="2" obis="0.1.94.34.14.255"/>
                                <set class="3" data="raw{06000015ae}" element="2" obis="0.1.94.34.15.255"/>
                                <set class="3" data="raw{0600001612}" element="2" obis="0.1.94.34.16.255"/>
                                <set class="20" data="raw{090C07D10101FF000000000800FF}" element="10" obis="0.0.13.0.1.255"/>
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