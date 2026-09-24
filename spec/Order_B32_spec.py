# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from expects import expect, equal
from primestg.utils import assertXMLEqual
from datetime import datetime

with description('Order B32 Generation'):
    with before.all:
        filenames = [
            'spec/data/B32_complete_example.xml',
            'spec/data/B32_remote_key_update.xml',
            'spec/data/B32_remote_key_update_2.xml',
            'spec/data/B32_update_master_key.xml',
            'spec/data/B32_init_meter.xml',
            'spec/data/B32_update_lls_after_field_operator_usage.xml',
        ]
        self.expected_results = []

        for filename in filenames:
            with open(filename) as f:
                xml_content = f.read()
                self.expected_results.append(xml_content)

    with it('generates expected B32 xml for complete example'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {
            'master_key': {'key_id': 3657378, 'key_wrap': 805398099580948550},
            'local_data_access_sec': [{'client_id': 1}, {'client_id': 2, 'secret': 66778899}],
            'remote_data_access_sec': {
                'client_id': 4, 'factory_secret': '2134B3FE', 'secret': '00ABCDEF',
                'data_transport_sec_keys': [{
                    'key_id': 5647378,
                    'key_type': 'GUnKey',
                    'key_val': '01010101010101010101010101010101',
                    'key_wrap': 805398099580948550,
                }, {
                    'key_id': 64838374,
                    'key_type': 'GAuKey',
                    'key_val': '01010101010101010101010101010101',
                    'key_wrap': 648763278468726487,
                }]
            }
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[0])

    with it('generates expected B32 xml for remote key update'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {
            'remote_data_access_sec': {
                'client_id': 4, 'factory_secret': '', 'secret': '00ABCDEF',
                'data_transport_sec_keys': [{
                    'key_id': 5647378,
                    'key_type': 'GUnKey',
                    'key_val': '85575445575837537',
                    'key_wrap': 805398099580948550,
                }, {
                    'key_id': 64838374,
                    'key_type': 'GAuKey',
                    'key_val': '75757875375875353',
                    'key_wrap': 648763278468726487,
                }]
            }
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[1])

    with it('generates expected B32 xml for remote key update 2'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'CCC0115108646',
            'version': '4.0',
        }
        payload = {
            'remote_data_access_sec': {
                'client_id': 4, 'factory_secret': '', 'secret': '00ABCDEF',
                'data_transport_sec_keys': [{
                    'key_id': 6478387,
                    'key_type': 'GUnKey',
                    'key_val': '9898327327877739',
                    'key_wrap': 805398099580948550,
                }, {
                    'key_id': 84368438,
                    'key_type': 'GAuKey',
                    'key_val': '3576536247457577',
                    'key_wrap': 648763278468726487,
                }]
            }
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[2])

    with it('generates expected B32 xml for update master key'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {
            'master_key': {'key_id': 35372772, 'key_wrap': 805398099580948550},
            'remote_data_access_sec': {
                'client_id': 4, 'factory_secret': '', 'secret': '',
                'data_transport_sec_keys': [{
                    'key_id': 6478387,
                    'key_type': 'GUnKey',
                    'key_val': '9898327327877739',
                    'key_wrap': 805398099580948550,
                }]
            }
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[3])

    with it('generates expected B32 xml for init meter'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {
            'local_data_access_sec': [
                {'client_id': 1, 'secret': 11223344},
                {'client_id': 2, 'secret': 66778899}
            ],
            'remote_data_access_sec': {
                'client_id': 4, 'factory_secret': '2134B3FE', 'secret': '00ABCDEF',
                'data_transport_sec_keys': [{
                    'key_id': 5647378,
                    'key_type': 'GUnKey',
                    'key_val': '85575445575837537',
                    'key_wrap': 805398099580948550,
                }, {
                    'key_id': 64838374,
                    'key_type': 'GAuKey',
                    'key_val': '75757875375875353',
                    'key_wrap': 648763278468726487,
                }]
            }
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[4])

    with it('generates expected B32 xml for updating lls'):
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {
            'local_data_access_sec': [{'client_id': 1, 'secret': 11223344}],
        }

        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, self.expected_results[5])

    with it('generates expected empty B32 xml'):
        expected_result = """
        <Order IdPet="11006811" IdReq="B32" Version="4.0">
            <Cnc Id="AAA57C4730016">
                <Cnt Id="BBB0115108646">
                    <B32>
                    </B32>
                </Cnt>
            </Cnc>
        </Order>
        """
        generic_values = {
            'id_pet': '11006811',
            'id_req': 'B32',
            'cnc': 'AAA57C4730016',
            'cnt': 'BBB0115108646',
            'version': '4.0',
        }
        payload = {}
        order = Order('B32')
        order = order.create(generic_values, payload)
        assertXMLEqual(order, expected_result)
