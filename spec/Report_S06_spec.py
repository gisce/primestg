from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S06 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/S06.xml',
            # 'spec/data/S06_empty.xml'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

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
        # result_filename = '{}_result.txt'.format(self.data_filename)
        #
        # with open(result_filename) as result_file:
        #     result_string = result_file.read()
        #     self.expected_result = literal_eval(result_string)
        #
        # result = self.report.values
        #
        # expect(result).to(equal(self.expected_result))
