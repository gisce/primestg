from expects import expect, equal
from primestg.report import Report
from primestg.message import MessageS
from switching.input.messages.TG import Concentrator, Values
from switching.input.messages.message import MessageTG


with description('Report S02 example'):
    with before.all:
        f = open('spec/data/CIR4621247027_0_S02_0_20150901111051')
        self.expected_firt_value_first_meter = [
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
        self.message_s = MessageS(f)

        self.message_tg = MessageTG(f)
        self.message_tg.parse_xml()

    with it('generates expected results for a value of the first meter of '
            'first contentrator'):
        report = Report(self.message_s)
        concentrator = report.concentrator[0]
        meter = concentrator.meter[0]
        values = meter.values

        first_value_first_meter = []
        for x in values:
            if x['timestamp'] == '2015-08-31 02:00:00':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(self.expected_firt_value_first_meter))

    with it('generates the expected results for a value of the first meter of '
            'first contentrator with switching'):
        concentrator = Concentrator(self.message_tg.obj.Cnc[0])
        meter = concentrator.get_meters()[0]
        values = Values(meter, 'S02', "3.1.c").get()

        first_value_first_meter = []
        for x in values:
            if x['timestamp'] == '2015-08-31 02:00:00':
                first_value_first_meter.append(x)

        expect(first_value_first_meter)\
            .to(equal(self.expected_firt_value_first_meter))

    with it('generates the same results of switching for the first meter'):
        switching_concentrator = Concentrator(self.message_tg.obj.Cnc[0])
        switching_meter = switching_concentrator.get_meters()[0]
        switching_meter_values = Values(switching_meter, 'S02', '3.1.c').get()

        report = Report(self.message_s)
        primestg_contentrator = report.concentrator[0]
        primestg_meter = primestg_contentrator.meter[0]
        primestg_meter_values = primestg_meter.values

        expect(primestg_meter_values).to(equal(switching_meter_values))
