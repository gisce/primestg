from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report S24 examples'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621511030_0_S24_0_20180529093051',
            'spec/data/CIR4621707229_0_S24_0_20180529200000',
            'spec/data/CIR4621707229_0_S24_0_20180529200000_warnings',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates result with the expected fields'):

        expected_first_value_first_concentrator = ['cnc_name', 'meters',
                                                   'season', 'timestamp']

        concentrator = list(self.report[0].concentrators)[0]
        parameter = concentrator.parameters[0]
        first_task_first_concentrator = parameter.values
        expect(sorted(first_task_first_concentrator))\
            .to(equal(expected_first_value_first_concentrator))

    with it('generates the expected results for all reports'):

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
        expect(len(warnings)).to(equal(1))
        expect(len(warnings[0])).to(equal(2))
