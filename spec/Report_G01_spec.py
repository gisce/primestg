from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report G01 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621531018_0_G01_0_20250531063000',
            'spec/data/CIR4621531018_0_G01_0_20250531063000_warnings',
            'spec/data/CIR4621531018_0_G01_0_20250531063000_empty',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates result with the expected fields'):

        expected_first_value_first_concentrator = {
            'season': 'S',
            'amed': 113,
            'tot': 117,
            'aperc': 94.87,
            'timestamp': '2025-05-30 07:00:00',
            'amax': 114,
        }
        concentrator = list(self.report[0].concentrators)[0]
        parameter = concentrator.parameters[0]
        first_task_first_concentrator = parameter.values
        expect(first_task_first_concentrator)\
            .to(equal(expected_first_value_first_concentrator))

    with it('generates the expected results for whole reports'):

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
