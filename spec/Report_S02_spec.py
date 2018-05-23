from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S02 example'):
    with before.all:

        self.data_filenames = [
            'spec/data/CIR4621247027_0_S02_0_20150901111051',
            'spec/data/CIR4621247027_0_S02_0_201509011empty',
            'spec/data/CIR4621247027_0_S02_0_20150901111051_warnings',
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            dict(
                ae=0,
                bc='00',
                ai=19,
                season='S',
                magn=1,
                name='CIR0141433184',
                r4=0,
                r1=11,
                r2=0,
                r3=0,
                timestamp='2015-08-31 02:00:00',
                cnc_name='CIR4621247027'
            )
        ]

        concentrator = list(self.report[0].concentrators)[0]
        meter = concentrator.meters[0]
        values = meter.values

        first_value_first_meter = []
        for x in values:
            if x['timestamp'] == '2015-08-31 02:00:00':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates expected result for a meter with error'):
        concentrator = list(self.report[0].concentrators)[0]
        result = concentrator.meters[17].values
        expect(result).to(equal([]))

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
        expected_warnings = [["WARNING: ['ERROR: Thrown exception: Date out of "
                             "range: 00001228230000W (Fh) year is out of range'"
                             "]", "WARNING: ['ERROR: Thrown exception: Date out"
                             " of range: 00001228230000W (Fh) year is out of ra"
                             "nge']", "WARNING: ['ERROR: Thrown exception: Date"
                             " out of range: 00001228230000W (Fh) year is out o"
                             "f range']", "WARNING: ['ERROR: Thrown exception: "
                             "Date out of range: 00001228230000W (Fh) year is o"
                             "ut of range']"]]
        expect(warnings).to(equal(expected_warnings))

