# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from primestg.utils import assertXMLEqual
from datetime import datetime

with description('Order B31 Generation'):
    with before.all:
        filenames = [
            'spec/data/B31.xml',
            'spec/data/B31_2.xml',
            'spec/data/B31_version_3_4.xml',
        ]
        self.expected_results = []

        for filename in filenames:
            with open(filename) as f:
                xml_content = f.read()
                self.expected_results.append(xml_content)

    with it('generates expected B31 xml for complete example'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B31',
            'cnc': 'AAA57C4730016',
            'version': '4.0',
        }
        payload = {
            'meters': [{
                'cnt': 'BBB0115108646', 'client_id': 4,
                'secret': '00ABCDEF', 'data_transport_sec_keys': [{
                    'key_id': 66365377, 'key_type': 'GUnKey', 'key_val': 805398099580948550,
                }, {
                    'key_id': 8373663, 'key_type': 'GAuKey', 'key_val': 648242389442428979,
                }]
            }, {
                'cnt': 'CCC0115108646', 'client_id': 4,
                'secret': '00ABCDEF', 'data_transport_sec_keys': [{
                    'key_id': 88747433, 'key_type': 'GUnKey', 'key_val': 805398099580948550,
                }, {
                    'key_id': 8474437, 'key_type': 'GAuKey', 'key_val': 648242389442428979,
                }]
            }],
        }

        order = Order('B31')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[0])

    with it('generates expected B31 xml for complete example 2'):
        generic_values = {
            'id_pet': '831',
            'id_req': 'B31',
            'cnc': 'ZZZ0000000001',
            'version': '4.0',
        }
        payload = {
            'meters': [{
                'cnt': 'XXX0219910832', 'client_id': 4,
                'secret': '00000005', 'data_transport_sec_keys': [{
                    'key_id': 5647378, 'key_type': 'GUnKey', 'key_val': '01010101010101010101010101010101',
                }, {
                    'key_id': 64838374, 'key_type': 'GAuKey', 'key_val': '02020202020202020202020202020202',
                }]
            }, {
                'cnt': 'XXX0219910833', 'client_id': 4,
                'secret': '00000005', 'data_transport_sec_keys': [{
                    'key_id': 5647378, 'key_type': 'GUnKey', 'key_val': '01010101010101010101010101010101',
                }, {
                    'key_id': 64838374, 'key_type': 'GAuKey', 'key_val': '02020202020202020202020202020202',
                }]
            }, {
                'cnt': 'XXX0219910834', 'client_id': 4,
                'secret': '00000005', 'data_transport_sec_keys': [{
                    'key_id': 5647378, 'key_type': 'GUnKey', 'key_val': '01010101010101010101010101010101',
                }, {
                    'key_id': 64838374, 'key_type': 'GAuKey', 'key_val': '02020202020202020202020202020202',
                }]
            }],
        }

        order = Order('B31')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[1])

    with it('generates expected v3.4 B31 xml'):
        generic_values = {
            'id_pet': '831',
            'id_req': 'B31',
            'cnc': 'ZZZ0000000001',
            'version': '3.4',
        }
        payload = {
            'meters': [{
                'cnt': 'XXX0219910832', 'client_id': 4,
                'activation_date': datetime(2013, 1, 1),
                'secret': '00000005', 'data_transport_sec_keys': [{
                    'key_id': 5647378, 'key_type': 'GUnKey', 'key_val': '01010101010101010101010101010101',
                }, {
                    'key_id': 64838374, 'key_type': 'GAuKey', 'key_val': '02020202020202020202020202020202',
                }]
            }, {
                'cnt': 'XXX0219910833', 'client_id': 4,
                'activation_date': datetime(2013, 1, 1),
                'secret': '00000005', 'data_transport_sec_keys': [{
                    'key_id': 5647378, 'key_type': 'GUnKey', 'key_val': '01010101010101010101010101010101',
                }, {
                    'key_id': 64838374, 'key_type': 'GAuKey', 'key_val': '02020202020202020202020202020202',
                }]
            }],
        }

        order = Order('B31')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[2])
