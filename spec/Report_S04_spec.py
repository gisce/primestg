from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S04 example'):
    with before.all:

        self.data_filename = 'spec/data/CIR4621247027_0_S04_0_20150901110412'

        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            {
                'r4': 2,
                'date_begin': '2015-08-01 00:00:00',
                'name': 'CIR0141433184',
                'r2': 0,
                'r3': 0,
                'ai': 308,
                'max': 471,
                'date_end': '2015-09-01 00:00:00',
                'period': 0,
                'contract': 1,
                'r1': 185,
                'cnc_name': 'CIR4621247027',
                'value': 'a',
                'ae': 0,
                'type': 'month',
                'date_max': '2015-08-08 13:00:00'
            }
        ]

        concentrator = self.report.concentrator[0]
        meter = concentrator.meter[0]
        values = meter.value

        first_value_first_meter = []
        for x in values:
            if x['period'] == 0 and x['value'] == 'a':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates the expected results for the whole report'):

        result_filename = '{}_result.txt'.format(self.data_filename)

        with open(result_filename) as result_file:
            result_string = result_file.read()
            self.expected_result = literal_eval(result_string)

        result = self.report.value

        expect(result).to(equal(self.expected_result))
