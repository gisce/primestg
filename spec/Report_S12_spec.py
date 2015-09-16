from expects import expect, equal
from primestg.report import Report
from primestg.message import MessageS
from ast import literal_eval


with description('Report S12 example'):
    with before.all:

        self.data_filename = 'spec/data/CIR4621247027_0_S12_0_20150903140000'

        with open(self.data_filename) as data_file:
            self.message_s = MessageS(data_file)

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

        report = Report(self.message_s)
        concentrator = report.concentrator[0]
        parameter = concentrator.parameter[0]
        first_task_first_concentrator = parameter.values[0]['tasks'][0]

        expect(first_task_first_concentrator)\
            .to(equal(expected_first_task_first_concentrator))

    with it('generates the expected results for the whole report'):

        result_filename = '{}_result.txt'.format(self.data_filename)

        with open(result_filename) as result_file:
            result_string = result_file.read()
            self.expected_result = literal_eval(result_string)

        result = Report(self.message_s).values

        expect(result).to(equal(self.expected_result))
