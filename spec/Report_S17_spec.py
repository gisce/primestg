from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report S17 examples'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0000035545_0_S17_0_20161203040002',
            'spec/data/ZIV0000035536_0_S17_0_20161204040002',
            'spec/data/ZIV0004311822_0_S17_0_20161215040002',
            'spec/data/ZIV0000035536_0_S17_0_201612040empty'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for the values of the the first '
            'concentrator'):

        expected_first_value_first_concentrator = \
            {
                'name': 'ZIV0000035545',
                'event_code': 1,
                'season': 'W',
                'timestamp': '2016-12-02 13:12:40:',
                'data': 'D1: admin\nD2: HMI_write',
                'event_group': 2
            }

        concentrator = list(self.report[0].concentrators)[0]
        parameter = concentrator.parameters[0]
        first_task_first_concentrator = parameter.values

        expect(sorted(first_task_first_concentrator))\
            .to(equal(sorted(expected_first_value_first_concentrator)))

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

