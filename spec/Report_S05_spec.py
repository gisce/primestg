from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S05 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621247027_0_S05_0_20150901072044',
            'spec/data/CIR4621247027_0_S05_0_201509010empty'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            {
                'r4': 2,
                'date_begin': '2015-09-01 00:00:00',
                'name': 'CIR0141433184',
                'r2': 0,
                'r3': 0,
                'ai': 308,
                'date_end': '2015-09-01 00:00:00',
                'period': 0,
                'contract': 1,
                'cnc_name': 'CIR4621247027',
                'value': 'a',
                'ae': 0,
                'type': 'day',
                'r1': 185
            }
        ]

        concentrator = self.report[0].concentrators[0]
        meter = concentrator.meters[0]
        values = meter.values

        first_value_first_meter = []
        for x in values:
            if x['name'] == 'CIR0141433184' and x['period'] == 0:
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates the expected results for the whole report'):

        result_filenames = []
        for data_filename in self.data_filenames:
            result_filenames.append('{}_result.txt'.format(data_filename))

        for key, result_filename in enumerate(result_filenames):
            with open(result_filename) as result_file:
                result_string = result_file.read()
                expected_result = literal_eval(result_string)

            result = self.report[key].values

            expect(result).to(equal(expected_result))
