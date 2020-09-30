from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with fdescription('Report S52 example'):
    with before.all:

        self.data_filename = 'spec/data/MRTR000000822522_0_S52_1_20200929001048'

        self.report = {}
        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates expected results for a value of the first line of '
            'first supervisor'):

        expected_first_value = dict(
            ae=0,
            bc='00',
            ai=8717,
            r1=43,
            r2=0,
            r3=0,
            r4=142,
            timestamp='2020-09-14 01:00:00'
        )

        supervisor = self.report.supervisors[0]
        line = supervisor.lines[0]
        values = line.values

        first_value_first_line = []
        for x in values:
            if x['timestamp'] == expected_first_value['timestamp']:
                first_value_first_line.append(x)

        expect(first_value_first_line)\
            .to(equal(expected_first_value))

    with it('generates expected result for a line with error'):
        supervisor = self.report.supervisors[0]
        result = supervisor.lines[5].values
        expect(result).to(equal([]))

    with it('generates the expected results for the whole report'):

        result_filenames = []
        warnings = []
        result_filenames.append('{}_result.txt'.format(self.data_filename))

        for key, result_filename in enumerate(result_filenames):
            result = []
            with open(result_filename) as result_file:
                result_string = result_file.read()
                expected_result = literal_eval(result_string)
            for supervisor in self.report.supervisors:
                if supervisor.lines:
                    for line in supervisor.lines:
                        for value in line.values:
                            result.append(value)
                        if line.warnings:
                            warnings.append(line.warnings)
            expect(result).to(equal(expected_result))
        line_found = 0
        for warning in warnings:
            if warning.get('MRTR000000822522', False):
                expect(len(list(warning.values())[0])).to(equal(4))
                line_found += 1
        expect(line_found).to(equal(2))
