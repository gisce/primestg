from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report S09 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0000034180_0_S09_0_20161216104003',
            'spec/data/ZIV0000034180_0_S09_0_20161216090401',
            'spec/data/ZIV0000034180_0_S09_0_20161216080308',
            'spec/data/ZIV0000034180_0_S09_0_201612160empty',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            {
                'name': 'ZIV0034631235',
                'timestamp': '2016-12-15 05:25:06',
                'cnc_name': 'ZIV0000034180',
                'season': 'W',
                'event_code': 1,
                'event_group': 6,
            }
        ]

        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values

        first_value_first_meter = []
        for x in values:
            if x['name'] == 'ZIV0034631235' and x['timestamp'] == \
                    '2016-12-15 05:25:06':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates the expected results for the whole report'):

        result_filenames = []
        for data_filename in self.data_filenames:
            result_filenames.append('{}_result.txt'.format(data_filename))

        for key, result_filename in enumerate(result_filenames):
            with open(result_filename) as result_file:
                result_string = result_file.read()
                expected_result = literal_eval(result_string)

            result = self.report[key].values

            expect(result).to(equal(expected_result))


