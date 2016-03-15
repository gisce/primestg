from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S06 example'):
    with before.all:

        self.data_filename = 'spec/data/S06.xml'

        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates the expected results for the whole report'):

        result_filename = '{}_result.txt'.format(self.data_filename)

        with open(result_filename) as result_file:
            result_string = result_file.read()
            self.expected_result = literal_eval(result_string)

        result = self.report.values

        expect(result).to(equal(self.expected_result))