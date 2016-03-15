from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S12 examples'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621247027_0_S12_0_20150903140000',
            'spec/data/ZIV0004338053_0_S12_0_20160309235002'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for the values of the first task of '
            'the first concentrator'):

        expected_first_task_first_concentrator = \
            {
                'task_data': [
                    {
                        'attributes': None,
                        'request': 'S02',
                        'stg_send': True,
                        'store': True
                    }
                ],
                'name': '1',
                'periodicity': '00000001000000',
                'date_from': '2015-09-04 01:10:00',
                'priority': 2,
                'meters': '',
                'complete': True
            }

        concentrator = self.report[0].concentrators[0]
        parameter = concentrator.parameters[0]
        first_task_first_concentrator = parameter.values['tasks'][0]

        expect(first_task_first_concentrator)\
            .to(equal(expected_first_task_first_concentrator))

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
