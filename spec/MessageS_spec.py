from expects import expect, raise_error, be_a
from primestg.message import MessageS
from lxml.objectify import ObjectifiedElement
from lxml.etree import XMLSyntaxError


with description('MessageS'):
    with it('raise an error if isn\'t provided an XML'):

        def callback():
            MessageS('foo bar')

        expect(callback).to(raise_error(XMLSyntaxError))

    with it('can parse an XML string'):
        message_s = MessageS('<xml><tag attr="var"/></xml>')
        expect(message_s.objectifyed).to(be_a(ObjectifiedElement))

    with it('can parse an XML file'):
        f = open('spec/data/CIR4621247027_0_S02_0_20150901111051')
        message_s = MessageS(f)
        expect(message_s.objectifyed).to(be_a(ObjectifiedElement))
