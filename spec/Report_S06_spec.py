from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S06 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/S06.xml',
            'spec/data/S06_with_error.xml',
            # 'spec/data/S06_empty.xml'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

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
                if cnc.meters:
                    for meter in cnc.meters:
                        for value in meter.values:
                            result.append(value)
                        if meter.warnings:
                            warnings.append(meter.warnings)

            expect(result).to(equal(expected_result))
        expected_warnings = [["ERROR: Cnc(CIR4621704174), "
                              "Meter(ZIV42553686). Thrown exception: "
                              "object of type 'NoneType' has no len()"]]
        expect(warnings).to(equal(expected_warnings))
