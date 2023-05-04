from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report S18 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0004426387_C208_S18_0_20230427134812',
            'spec/data/ZIV0004426387_C208_S18_0_20230427134812empty'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = {
                'orden': 0,
                'cnc_name': 'ZIV0004426387',
                'name': 'ORB0000859879',
                'order_datetime': '2023-04-21 10:55:00'
        }


        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values[0]

        expect(values['cnc_name']).to(equal(expected_first_value_first_meter['cnc_name']))
        expect(values['name']).to(equal(expected_first_value_first_meter['name']))
        expect(values['orden']).to(equal(expected_first_value_first_meter['orden']))
        expect(values['order_datetime']).to(equal(expected_first_value_first_meter['order_datetime']))


