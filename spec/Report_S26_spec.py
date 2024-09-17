from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S26 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/S26.xml',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            {
                'timestamp': '2024-09-09 11:58:58',
                'active_quadrant': 0,
                'current_sum_3_phases': 23.0,

                'voltage1': 239,
                'current1': 0.0,
                'active_power_import1': 0,
                'active_power_export1': 1510,
                'reactive_power_import1': 0,
                'reactive_power_export1': 0,
                'power_factor1': 0.0,
                'active_quadrant_phase1': 0,

                'voltage2': 0.0,
                'current2': 0.0,
                'active_power_import2': 0,
                'active_power_export2': 0,
                'reactive_power_import2': 0,
                'reactive_power_export2': 0,
                'power_factor2': 0.0,
                'active_quadrant_phase2': 0,

                'voltage3': 0.0,
                'current3': 0.0,
                'active_power_import3': 0,
                'active_power_export3': 0,
                'reactive_power_import3': 0,
                'reactive_power_export3': 0,
                'power_factor3': 0.0,
                'active_quadrant_phase3': 0,

                'phase_presence': [0],
                'meter_phase': 0,
                'current_switch_state': 0,
                'previous_switch_state': 0,

                'ai': 0,
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