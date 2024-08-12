from expects import expect, equal
from primestg.report import Report


with description('Report S53 example'):
    with before.all:

        self.data_filename = 'spec/data/ORMR208231717738_0_S53_1_20240624050827'

        self.report = {}
        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates expected results for a value of the first line supervisor of '
            'first remote terminal unit'):

        expected_first_value = dict(
            ai1=2978.0,
            ai2=4171.0,
            ai3=2601.0,
            ae1=0.0,
            ae2=0.0,
            ae3=0.0,
            r11=225.0,
            r12=973.0,
            r13=201.0,
            r21=0.0,
            r22=0.0,
            r23=0.0,
            r31=0.0,
            r32=0.0,
            r33=0.0,
            r41=0.0,
            r42=0.0,
            r43=0.0,
            bc='00',
            timestamp='2024-06-24 05:00:00',
            rt_unit_name='ORMR208231717738',
            name='ORML208231065728',
            magn=1
        )

        rt_unit = list(self.report.rt_units)[0]
        line_supervisor = list(rt_unit.line_supervisors)[0]
        values = line_supervisor.values

        first_value_first_line_supervisor = {}
        for x in values:
            if x['timestamp'] == expected_first_value['timestamp']:
                first_value_first_line_supervisor = x

        expect(first_value_first_line_supervisor)\
            .to(equal(expected_first_value))
