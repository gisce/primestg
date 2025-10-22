from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report G01 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621531018_0_G02_0_20250625070000',
            'spec/data/CIR4621531018_0_G02_0_20250625070000_warnings',
            'spec/data/CIR4621531018_0_G02_0_20250625070000_empty',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates result with the expected fields'):

        expected_first_value_first_meter = [
            {
                'atimeperc': 100.0,
                'cnc_name': 'CIR4621531018',
                'nchanges': 0,
                'name': 'CIR2081531008',
                'season': 'S',
                'timestamp': '2025-06-25 00:00:00',
                'atime': 1439,
                'ahourly': '',
                'aconc': 1439
            }
        ]
        concentrator = list(self.report[0].concentrators)[0]
        parameter = concentrator.meters[0]
        first_task_first_concentrator = parameter.values
        expect(first_task_first_concentrator)\
            .to(equal(expected_first_value_first_meter))

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
                if cnc.meters:
                    for meter in cnc.meters:
                        for value in meter.values:
                            result.append(value)
                        if meter.warnings:
                            warnings.append(meter.warnings)
                expect(result).to(equal(expected_result))
        total_warnings = 0
        for warning in warnings:
            if warning.get('CIR2081531008', False):
                expect(len(list(warning.values())[0])).to(equal(1))
                total_warnings += 1
            if warning.get('LGZ0012240491', False):
                expect(len(list(warning.values())[0])).to(equal(1))
                total_warnings += 1
        expect(total_warnings).to(equal(3))
