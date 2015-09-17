from expects import expect, equal
from primestg.report import Report
from ast import literal_eval


with description('Report S02 example'):
    with before.all:

        self.data_filename = 'spec/data/CIR4621247027_0_S02_0_20150901111051'

        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates expected results for a value of the first meter of '
            'first concentrator'):

        expected_first_value_first_meter = [
            dict(
                ae=0.0,
                bc='00',
                ai=19.0,
                season='S',
                magn=1,
                name='CIR0141433184',
                r4=0.0,
                r1=11.0,
                r2=0.0,
                r3=0.0,
                timestamp='2015-08-31 02:00:00'
            )
        ]

        concentrator = self.report.concentrator[0]
        meter = concentrator.meter[0]
        values = meter.values

        first_value_first_meter = []
        for x in values:
            if x['timestamp'] == '2015-08-31 02:00:00':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(expected_first_value_first_meter))

    with it('generates expected result for a meter with error'):
        result = self.report.concentrator[0].meter[17].values
        expect(result).to(equal({}))

    with it('generates the expected results for the whole report'):

        result_filename = '{}_result.txt'.format(self.data_filename)

        with open(result_filename) as result_file:
            result_string = result_file.read()
            self.expected_result = literal_eval(result_string)

        result = self.report.values

        expect(result).to(equal(self.expected_result))
