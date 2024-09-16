from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S07 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/S07.xml',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of first concentrator'):

        expected_first_value_first_meter = [
            dict(
                timestamp='2024-01-03 00:27:19',
                season='W',
                dc=180,
                nc=54,
                df=23433,
                hc='2023-12-24 11:22:41',
                cnc_name='CIR4622119033',
                name='SAG0155354621'
            )
        ]

        concentrator = list(self.report[0].concentrators)[0]
        values = concentrator.meters[0].values

        expect(values).to(equal(expected_first_value_first_meter))

    with it('generates expected result for a meter with error'):
        concentrator = list(self.report[0].concentrators)[0]
        result = concentrator.meters[-1].values
        expect(result).to(equal([]))
