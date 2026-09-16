from primestg.model_manufacturer import get_marcas_dict
from expects import expect, have_keys, be_a, equal

with description('Parse manufacturer models'):

    with before.all:
        self.products = []


    with it('Get marcas'):
        marcas = get_marcas_dict()

        expect(marcas).to(be_a(dict))
        expect(marcas).to(have_keys('9', 'C'))

        expect(marcas['9']).to(equal('SOGECAM'))
        expect(marcas['C']).to(equal('LANDIS'))