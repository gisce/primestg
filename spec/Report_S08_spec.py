from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S08 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/S08.xml',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of first concentrator'):

        expected_first_value_first_meter = [
            {
                'timestamp': '2024-01-02 18:36:58',
                'season': 'W',
                'cnc_name': 'CIR4622119033',
                'name': 'SAG0155354713',
                'nsubtt': 1142,
                'tsubtt': 27944,
                'tsubta': 14,
                'nsubtf1': 1142,
                'tsubtf1': 96672,
                'tsubtf1a': 0,
                'nsubtf2': 0,
                'tsubtf2': 0,
                'tsubtf2a': 0,
                'nsubtf3': 0,
                'tsubtf3': 0,
                'tsubtf3a': 0,
                'nsobtt': 5149,
                'tsobtt': 64095,
                'tsobta': 4,
                'nsobtf1': 5149,
                'tsobtf1': 64095,
                'tsobtf1a': 0,
                'nsobtf2': 0,
                'tsobtf2': 0,
                'tsobtf2a': 0,
                'nsobtf3': 0,
                'tsobtf3': 0,
                'tsobtf3a': 0,
                'ncortett': 52,
                'tcortett': 178,
                'tcorteta': 0,
                'ncortetf1': 0,
                'tcortetf1': 0,
                'tcortetf1a': 0,
                'ncortetf2': 0,
                'tcortetf2': 0,
                'tcortetf2a': 0,
                'ncortetf3': 0,
                'tcortetf3': 0,
                'tcortetf3a': 0,
            }
        ]

        concentrator = list(self.report[0].concentrators)[0]
        values = concentrator.meters[0].values

        expect(values).to(equal(expected_first_value_first_meter))

    with it('generates expected result for a meter with error'):
        concentrator = list(self.report[0].concentrators)[0]
        result = concentrator.meters[-1].values
        expect(result).to(equal([]))
