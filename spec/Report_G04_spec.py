from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report G04 example'):
    with before.all:

        data_filename = 'spec/data/CIR4621511370_0_G04_0_20260922081142'
        with open(data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates result with the expected fields'):

        first_value_meter = {
            'timestamp': '2026-09-15 04:00:00',
            'season': 'S',
            'bc': '82',
            'ineutral': 10.7,
            'v1': 137,
            'v2': 137,
            'v3': 137,
            'i1': 122.9,
            'i2': 115.9,
            'i3': 126.1,
            'name': 'CIR2081429002',
            'cnc_name': 'CIR4621511370'
        }
        concentrator = list(self.report.concentrators)[0]
        parameter = concentrator.meters[0]
        first_task_first_concentrator = parameter.values[0]
        expect(first_task_first_concentrator)\
            .to(equal(first_value_meter))
