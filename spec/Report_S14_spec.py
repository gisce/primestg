from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report S14 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIVS004394488_0_S14_20230510100000',
            'spec/data/ZIVS004394488_0_S14_20230510100000empty'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = {
            'cnc_name': 'ZIV0004394488',
            'name': 'ZIVS004394488',
            'timestamp': '2023-05-08 12:00:00',
            'season': 'S',
            'bc': 'd0',
            'simp': 0,
            'sexp': 0,
            'v1': 228,
            'v2': 0,
            'v3': 0,
            'i1': 0,
            'i2': 0,
            'i3': 0,
            'in': 0
        }

        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values[0]

        for key in values.keys():
            expect(values[key]).to(equal(expected_first_value_first_meter[key]))


