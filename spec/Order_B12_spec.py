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

    with it('generates expected B12 Latent Tariff 2.0TD definition'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">
                  <Cnc Id="CIR4621544074">
                    <Cnt Id="CNT000000000">
                      <B12 Ffin="" Fini="">
                        <set class="20" data="raw{01010203090101090cffff0101ff00000000800000090101}" element="7" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{010102080901011101110111011101110111021102}" element="8" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{0102020211010106020309040000000009060100003001ff120003020309040800000009060100003001ff120002020309040a00000009060100003001ff120001020309040e00000009060100003001ff120002020309041200000009060100003001ff120001020309041600000009060100003001ff120002020211020101020309040000000009060100003001ff120003}" element="9" obis="0.0.13.0.1.255"/>
                        <set class="11" data="raw{010902031200010905FFFF0101FF110202031200080905FFFF0106FF110202031200020905FFFF0501FF110202031200030905FFFF080FFF110202031200040905FFFF0A0CFF110202031200050905FFFF0B01FF110202031200060905FFFF0C06FF110202031200070905FFFF0C08FF110202031200080905FFFF0C19FF1102}" element="2" obis="0.0.11.0.4.255"/>
                        <set class="20" data="raw{090C07E50601FF000000000800FF}" element="10" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{090633545F544441}" element="6" obis="0.0.13.0.1.255"/>
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
            'template': 'TAR_20TD',
            'date': date(2021, 6, 1),
            'date_from': '',
            'date_to': '',

        }

        order = Order('B12')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)

    with it('generates expected B12 Latent Tariff Tariff 3.0TD definition'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">
                  <Cnc Id="CIR4621544074">
                    <Cnt Id="CNT000000000">
                      <B12 Ffin="" Fini="">
                        <set class="20" data="raw{01090203090101090cffff0101ff000000008000000901010203090102090cffff0301ff000000008000000901020203090103090cffff0401ff000000008000000901030203090104090cffff0601ff000000008000000901040203090105090cffff0701ff000000008000000901010203090106090cffff0801ff000000008000000901040203090107090cffff0a01ff000000008000000901030203090108090cffff0b01ff000000008000000901020203090109090cffff0c01ff00000000800000090101}" element="7" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{010402080901011101110111011101110111051105020809010211021102110211021102110511050208090103110411041104110411041105110502080901041103110311031103110311051105}" element="8" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{0105020211010106020309040000000009060100003001ff120006020309040800000009060100003001ff120002020309040900000009060100003001ff120001020309040e00000009060100003001ff120002020309041200000009060100003001ff120001020309041600000009060100003001ff120002020211020106020309040000000009060100003001ff120006020309040800000009060100003001ff120003020309040900000009060100003001ff120002020309040e00000009060100003001ff120003020309041200000009060100003001ff120002020309041600000009060100003001ff120003020211030106020309040000000009060100003001ff120006020309040800000009060100003001ff120004020309040900000009060100003001ff120003020309040e00000009060100003001ff120004020309041200000009060100003001ff120003020309041600000009060100003001ff120004020211040106020309040000000009060100003001ff120006020309040800000009060100003001ff120005020309040900000009060100003001ff120004020309040e00000009060100003001ff120005020309041200000009060100003001ff120004020309041600000009060100003001ff120005020211050101020309040000000009060100003001ff120006}" element="9" obis="0.0.13.0.1.255"/>
                        <set class="11" data="raw{010902031200010905FFFF0101FF110502031200080905FFFF0106FF110502031200020905FFFF0501FF110502031200030905FFFF080FFF110502031200040905FFFF0A0CFF110502031200050905FFFF0B01FF110502031200060905FFFF0C06FF110502031200070905FFFF0C08FF110502031200080905FFFF0C19FF1105}" element="2" obis="0.0.11.0.4.255"/>
                        <set class="20" data="raw{090C07E50B19FF000000000800FF}" element="10" obis="0.0.13.0.1.255"/>
                        <set class="20" data="raw{090636545F544441}" element="6" obis="0.0.13.0.1.255"/>
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
            'template': 'TAR_30TD',
            'date': date(2021, 11, 25),
            'date_from': '',
            'date_to': '',

        }

        order = Order('B12')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)

    with it('generates expected B12 read trafo ratio'):
        expected_result = (
            """<Order IdPet="1234" IdReq="B12" Version="3.1.c">
                  <Cnc Id="CIR4621544074">
                    <Cnt Id="CNT000000000">
                      <B12 Ffin="" Fini="">
                        <get class="1" element="2" obis="1.0.0.4.2.255"/>
                        <get class="1" element="2" obis="1.0.0.4.3.255"/>
                        <get class="1" element="2" obis="1.0.0.4.5.255"/>
                        <get class="1" element="2" obis="1.0.0.4.6.255"/>
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
            'template': 'TRAFO_RATIO',
            'date': date(2021, 11, 25),
            'date_from': '',
            'date_to': '',

        }

        order = Order('B12')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)