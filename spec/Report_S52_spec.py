from expects import expect, equal
from primestg.report import Report


with fdescription('Report S52 example'):
    with before.all:

        self.data_filename = 'spec/data/MRTR000000822522_0_S52_1_20200929001048'

        self.report = {}
        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates expected results for a value of the first line of '
            'first remote terminal unit'):

        expected_first_value = dict(
            ae=0.0,
            bc='00',
            ai=8717.0,
            r1=43.0,
            r2=0.0,
            r3=0.0,
            r4=142.0,
            timestamp='2020-09-14 01:00:00',
            rt_unit_name='MRTR000000822522',
            name='MRTL000006609121',
            magn=1
        )

        rt_unit = self.report.rt_units[0]
        line = rt_unit.lines[0]
        values = line.values

        first_value_first_line = {}
        for x in values:
            if x['timestamp'] == expected_first_value['timestamp']:
                first_value_first_line = x

        expect(first_value_first_line)\
            .to(equal(expected_first_value))
