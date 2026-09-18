# -*- coding: utf-8 -*-
from expects import expect, equal
from primestg.report import Report


with description('Report S31 example'):
    with before.all:
        self.data_filenames = [
            'spec/data/S31.xml',
            'spec/data/S31_bad_date.xml',
            'spec/data/S31_empty.xml',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of first concentrator'):
        expected_first_value_first_meter = [{
            'concentrator': 'AAA79DE402219',
            'meter': 'BBB0135084421',
            'version': '4.0',
            'request_id': '0',

            'timestamp': '2013-07-12 13:00:00',
            'season': 'S',
            'client_id': 4,
            'status': 0,
            'key_request': '00111101',
            'lls_opt_rea': 1,
            'lls_opt_sec': 1,
            'lls_plc': 1,
            'gaukey': 1,
            'gbrkey': 0,
            'gunkey': 1,
            'cdt_sec_cur': [{
                'key_id': 253673732,
                'key_type': 'GUnKey',
            }, {
                'key_id': 5363527,
                'key_type': 'GAuKey',
            }],
        }]

        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values
        expect(values).to(equal(expected_first_value_first_meter))

    with it('generates the expected results for the whole report'):
        expected_total = [{
            'concentrator': 'AAA79DE402219',
            'meter': 'BBB0135084421',
            'version': '4.0',
            'request_id': '0',

            'timestamp': '2013-07-12 13:00:00',
            'season': 'S',
            'client_id': 4,
            'status': 0,
            'key_request': '00111101',
            'lls_opt_rea': 1,
            'lls_opt_sec': 1,
            'lls_plc': 1,
            'gaukey': 1,
            'gbrkey': 0,
            'gunkey': 1,
            'cdt_sec_cur': [{
                'key_id': 253673732,
                'key_type': 'GUnKey',
            }, {
                'key_id': 5363527,
                'key_type': 'GAuKey',
            }],
        }, {
            'concentrator': 'AAA79DE402219',
            'meter': 'CCC0135084421',
            'version': '4.0',
            'request_id': '0',

            'status': 1,
            'key_request': '00001101',
            'lls_opt_rea': 0,
            'season': 'S',
            'gunkey': 1,
            'lls_opt_sec': 0,
            'lls_plc': 1,
            'gbrkey': 0,
            'client_id': 4,
            'timestamp': '2013-07-12 13:15:00',
            'cdt_sec_cur': [],
            'gaukey': 1,
        }]
        values = self.report[0].values
        expect(values).to(equal(expected_total))

    with it('generates the expected exception when an error occurs'):
        expected_warnings = [
            {
                'BBB0135084421': [
                    "ERROR: Thrown exception: Date out of range: 20000S (Fh) invalid literal for int() with base 10: '0S'"
                ]
            }
        ]
        expected_result = [{
            'concentrator': 'AAA79DE402219',
            'meter': 'CCC0135084421',
            'version': '4.0',
            'request_id': '0',

            'status': 1,
            'key_request': '00001101',
            'lls_opt_rea': 0,
            'season': 'S',
            'gunkey': 1,
            'lls_opt_sec': 0,
            'lls_plc': 1,
            'gbrkey': 0,
            'client_id': 4,
            'timestamp': '2013-07-12 13:15:00',
            'cdt_sec_cur': [],
            'gaukey': 1,
        }]

        concentrator = list(self.report[1].concentrators)[0]
        values = concentrator.values
        warnings = concentrator.warnings
        expect(warnings).to(equal(expected_warnings))
        expect(values).to(equal(expected_result))

        meter_values_1 = concentrator.meters[0].values
        meter_warnings_1 = concentrator.meters[0].warnings
        meter_values_2 = concentrator.meters[1].values
        meter_warnings_2 = concentrator.meters[1].warnings
        expect(meter_warnings_1).to(equal(expected_warnings[0]))
        expect(meter_warnings_2).to(equal({}))

    with it('generates the expected report for an empty concentrator'):
        values = self.report[2].values
        expect(values).to(equal([]))
