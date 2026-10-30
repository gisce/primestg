# -*- coding: utf-8 -*-
from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S32 example'):
    with before.all:
        self.data_filenames = [
            'spec/data/S32.xml',
            'spec/data/S32_with_error.xml'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for the values of the the first  concentrator'):
        expected_first_value_first_concentrator = {
            'name': 'XXX0004427746',
            'event_code': 1,
            'event_group': 5,
            'season': 'S',
            'timestamp': '2022-07-07 12:15:12',
            'D1': 'XXX0036491967',
            'D2': {'010000600100FF02': '30303336343931393637', '010000600102ff02': '636f6e7461646f722020444c4d5330313038', '010000600101ff02': '205a50503232'},
        }

        concentrator = list(self.report[0].concentrators)[0]
        parameter = concentrator.parameters[0]
        first_task_first_concentrator = parameter.values
        expect(first_task_first_concentrator).to(equal(expected_first_value_first_concentrator))

    with it('generates the expected results for the whole report'):
        result_filenames = []
        warnings = []
        for data_filename in self.data_filenames:
            result_filenames.append('{}_result.txt'.format(data_filename))

        for key, result_filename in enumerate(result_filenames):
            result = []
            with open(result_filename) as result_file:
                result_string = result_file.read()
                expected_result = literal_eval(result_string)
            for cnc in self.report[key].concentrators:
                for value in cnc.values:
                    result.append(value)
                if cnc.warnings:
                    warnings.append(cnc.warnings)
                expect(result).to(equal(expected_result))
