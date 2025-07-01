from primestg.cycle.cycles import CycleFile
from primestg.utils import DLMSTemplates
from expects import expect, equal, contain
import io
from datetime import datetime

from primestg.report import Report
from ast import literal_eval


with description('Parse CNC cycles'):

    with before.all:

        self.data_filenames = [
            'spec/data/Ciclo_instant_data_minute_20241129_112335_0.csv',
            'spec/data/Ciclo_instant_data_minute_20241129_124027.csv',
            'spec/data/Ciclo_TAR_20TD_raw_20241129_102357_0.csv',
        ]

        self.expected_data = [
            # obis 0.0.21.0.5.255 one register
            [
                {
                    'timestamp': datetime(2024, 11, 29, 11, 23, 36),
                    'reg_name': 'SAG0155349819',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    'data': ['2024/11/29 11:23:30', '224', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1000']
                 }
            ],
            # obis 0.0.21.0.5.255 various registers
            [
                {
                    'timestamp': datetime(2024, 11, 29, 12, 40, 6),
                    'reg_name': 'CIR2081710470',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    #         clock               , v1   , i1   , v2   , i2   , v3   , i3   , sum i , inPot , outP, inR  , outR, powerF
                    'data': ['2024/11/29 12:40:09', '235', '409', '235', '326', '236', '337', '1074', '1211', '0', '1964', '0', '520'],
                },
                {
                    'timestamp': datetime(2024, 11, 29, 12, 40, 9),
                    'reg_name': 'CIR0501516020',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    'data': ['2024/11/29 12:40:10', '136', '0', '142', '0', '139', '0', '0', '0', '0', '0', '0', '1000'],
                },
                {
                    'timestamp': datetime(2024, 11, 29, 12, 40, 10),
                    'reg_name': 'ITE0131750581',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    'data': ['2024/11/29 12:40:10', '232', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1000'],
                },
                {
                    'timestamp': datetime(2024, 11, 29, 12, 40, 12),
                    'reg_name': 'SAG0186255184',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    'data': ['2024/11/29 12:40:13', '235', '0', '234', '0', '234', '0', '0', '0', '0', '0', '0', '1000']
                },
                {
                    'timestamp': datetime(2024, 11, 29, 12, 40, 21),
                    'reg_name': 'ZIV0034703466',
                    'operation': 'get',
                    'obis': '0.0.21.0.5.255',
                    'class_id': 7,
                    'element_id': 2,
                    'data': ['2024/11/29 12:40:17', '133', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                },
            ],
            # Failed get
            [
                {
                    'timestamp': datetime(2024, 11, 29, 10, 23, 57),
                    'reg_name': 'ZIV0040318130',
                    'operation': '',
                    'obis': '',
                    'class_id': None,
                    'element_id': None,
                    'data': []
                 }
            ],

        ]

    with it('Parses all files and content'):
        for path in self.data_filenames:
            from_path = CycleFile(path=path)

            with io.open(path, encoding='utf-8') as fp:
                content = fp.read()
                from_text = CycleFile(content=content)

            expect(from_path.data).to(equal(from_text.data))

    with it('Returns expected dict'):
        for index in range(0, len(self.expected_data)):
            c = CycleFile(path=self.data_filenames[index])
            expected_list = self.expected_data[index]

            expect(len(c.data)).to(equal(len(expected_list)))
            for element_index in range(0, len(expected_list)):
                cycle_data = c.data[element_index]
                expected = expected_list[element_index]
                expect(expected['timestamp']).to(equal(cycle_data['timestamp']))
                expect(expected['reg_name']).to(equal(cycle_data['reg_name']))
                expect(expected['operation']).to(equal(cycle_data['operation']))
                expect(expected['obis']).to(equal(cycle_data['obis']))
                expect(expected['class_id']).to(equal(cycle_data['class_id']))
                expect(expected['element_id']).to(equal(cycle_data['element_id']))
                expect(len(expected['data'])).to(equal(len(cycle_data['data'])))
                for i in range(0, len(cycle_data['data'])):
                    expect(expected['data'][i]).to(equal(cycle_data['data'][i]))

with description("Function generate_cycles with GET_INSTANT"):

    with it("Generar correctament un cicle DLMS"):

        generator = DLMSTemplates()
        meters = ['123456789']
        xml = generator.generate_cycles(
            template_name='GET_INSTANT',
            meters_name=meters,
            period='15',
            immediate='false',
            repeat='96'
        )

        expect(xml).to(contain('<cycle name="Cicle_GET_INSTANT_raw" period="15" immediate="false" repeat="96" priority="1">'))
        expect(xml).to(contain('<device sn="123456789"/>'))
        expect(xml).to(contain('<get obis="0.0.21.0.5.255" class="7" element="2"/>'))
        expect(xml).to(contain('</cycle>'))




