from expects import expect, raise_error, be_a
from primestg.report import Report
from primestg.message import MessageS


with description('Report'):
    with it('raise an error if isn\'t provided a file, basestring or '
            'MessageS'):

        def callback():
            Report([])

        error = 'must be file or basestring with XML or a MessageS'
        expect(callback).to(raise_error(TypeError, error))

    with it('can parse an XML string'):
        report = Report('<xml><tag attr="var"/></xml>')
        expect(report.message).to(be_a(MessageS))

    with it('can parse an XML file'):
        with open('spec/data/CIR4621247027_0_S02_0_20150901111051') as f:
            report = Report(f)
        expect(report.message).to(be_a(MessageS))

    with it('accepts a MessageS directly'):
        with open('spec/data/CIR4621247027_0_S04_0_20150901110412') as f:
            message_s = MessageS(f)
        report = Report(message_s)
        expect(report.message).to(be_a(MessageS))
