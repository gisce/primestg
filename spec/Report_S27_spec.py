from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S27 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0004394488_0_S27_20170727120456_no_max',
            'spec/data/ZIV0004395680_0_S27_20181031164412_with_max',
            # 'spec/data/CIR4621247027_0_S05_0_20150901072044_warnings',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a meter with values at 0'):

        expected_first_value_first_meter = [
            {
                'r4': 0,
                'date_begin': '2017-07-27 12:04:56',
                'name': 'ZIVS004394488',
                'r2': 0,
                'r3': 0,
                'ai': 0,
                'date_end': '2017-07-27 12:04:56',
                'period': 0,
                'contract': 1,
                'cnc_name': 'ZIV0004394488',
                'value': 'a',
                'ae': 0,
                'type': 'manual',
                'r1': 0,
                'max': 0,
                'date_max': '2017-07-14 08:39:00'
            }
        ]
        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values
        first_value_first_meter = []
        for x in values:
            if x['name'] == 'ZIVS004394488' and x['period'] == 0:
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates expected results for a meter with real values'):

        expected_first_value_first_meter = [
            {
                'r4': 610,
                'date_begin': '2018-10-31 16:44:12',
                'name': 'ZIV0044510398',
                'r2': 0,
                'r3': 0,
                'ai': 3568,
                'date_end': '2018-10-31 16:44:12',
                'period': 0,
                'contract': 1,
                'cnc_name': 'ZIV0004395680',
                'value': 'a',
                'ae': 0,
                'type': 'manual',
                'r1': 2688,
                'max': 4744,
                'date_max': '2018-10-06 23:15:00'
            }
        ]
        concentrator = list(self.report[1].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values
        first_value_first_meter = []
        for x in values:
            if x['name'] == 'ZIV0044510398' and x['period'] == 0:
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

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
        meter_found = 0
        for warning in warnings:
            if warning.get('ZIV0044510398', False):
                expect(len(list(warning.values())[0])).to(equal(2))
                meter_found += 1
        expect(meter_found).to(equal(0))
