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
        expect(message_s.objectified).to(be_a(ObjectifiedElement))

    with it('can parse an XML file'):
        filename = 'spec/data/CIR4621247027_0_S02_0_20150901111051'
        with open(filename) as data_file:
            message_s = MessageS(data_file)
        expect(message_s.objectified).to(be_a(ObjectifiedElement))
