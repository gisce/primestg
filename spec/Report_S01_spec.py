from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S01 example'):

    with before.all:

        self.data_filenames = [
            'spec/data/S01.xml',
            'spec/data/S01_empty.xml',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of first concentrator'):

        expected_first_value_first_meter = [
            {
                'timestamp': '2019-10-15 15:26:17',
                'voltage': 230,
                'current': 0.0,
                'active_power_import': 1870,
                'active_power_export': 0,
                'reactive_power_import': 0,
                'reactive_power_export': 50,
                'power_factor': 1.0,
                'active_quadrant': 4,
                'phase_presence': [1, 2, 3],
                'meter_phase': 5,
                'current_switch_state': 1,
                'previous_switch_state': 1,
                'ai': 2,
                'ae': 0,
                'r1': 0,
                'r2': 0,
                'r3': 0,
                'r4': 0,
                'cnc_name': 'ZIV0004366654',
                'name': 'ZIV0044548861',
            }
        ]

        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values
        expect(values).to(equal(expected_first_value_first_meter))

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
