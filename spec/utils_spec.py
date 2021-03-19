# -*- coding: utf-8 -*-
from expects import expect, raise_error, be_a, equal
from primestg.utils import DLMSTemplates, ContractTemplates, datetohexprime, octet2name, name2octet
from primestg.dlms_templates import DLMS_TEMPLATES
from datetime import date


with description('Utils'):
    with context("DLMSTemplates"):
        with context('get_available_templates'):
            with it('returns all templates list of tuples'):
                dt = DLMSTemplates()
                retrieved = dt.get_available_templates()
                retrieved_names = [t[0] for t in retrieved]

                available_templates = DLMS_TEMPLATES
                available_names = [t for t in available_templates.keys()]

                expect(available_names).to(equal(retrieved_names))

            with it('returns only selected category templates'):
                all_templates = DLMS_TEMPLATES
                available_categories = list(set([t['category'] for t in all_templates.values()]))

                dt = DLMSTemplates()

                for category in available_categories:
                    retrieved = dt.get_available_templates(template_type=category)
                    retrieved_names = [t[0] for t in retrieved]

                    available_names = [n for n, t in all_templates.items() if t['category'] == category]
                    expect(available_names).to(equal(retrieved_names))

            with it('returns only selected origin templates'):
                all_templates = DLMS_TEMPLATES
                available_origins = list(set([t['origin'] for t in all_templates.values()]))

                dt = DLMSTemplates()

                for origin in available_origins:
                    retrieved = dt.get_available_templates(origin=origin)
                    retrieved_names = [t[0] for t in retrieved]

                    available_names = [n for n, t in all_templates.items() if t['origin'] == origin]
                    expect(available_names).to(equal(retrieved_names))

            with it('returns only selected origin and category templates'):
                all_templates = DLMS_TEMPLATES

                dt = DLMSTemplates()

                category = 'contract'
                origin = 'library'
                retrieved = dt.get_available_templates(origin=origin, template_type=category)
                retrieved_names = [t[0] for t in retrieved]

                available_names = [n for n, t in all_templates.items()
                                   if t['origin'] == origin and t['category'] == category]

                expect(available_names).to(equal(retrieved_names))

    with context("datetohexprime"):
        with it('returns an hexadecimal date'):
            dts = {
                '07E40B01': date(2020, 11, 1),
                '07E50401': date(2021, 4, 1),
                '07E50601': date(2021, 6, 1),
                '07B60410': date(1974, 4, 16),
                '07E60C19': date(2022, 12, 25),
                '07D10101': date(2001, 1, 1),
            }
            for res, dt in dts.items():
                expect(res).to(equal(datetohexprime(dt)))

    with context("octet2name"):
        with it("returns a text"):
            names = {
                "000000000000": '',
                "202020202020": '      ',
                "202020444833": '   DH3',
                "2020322E3041": '  2.0A',
                "322E30412020": '2.0A  ',
                "322E30444841": '2.0DHA',
                "322E305F5354": '2.0_ST',
                "324153544152": '2ASTAR',
                "332E302E3220": '3.0.2 ',
                "332E30413650": '3.0A6P',
                "33545F544441": '3T_TDA',
                "363353544152": '63STAR',
                "36545F544441": '6T_TDA',
                "414354495645": 'ACTIVE',
                "43414C303032": 'CAL002',
                "43414C303033": 'CAL003',
                "4448320031FF": 'DH2',
                "444841000000": 'DHA',
                "4448415F4954": 'DHA_IT',
                "4448415F5544": 'DHA_UD',
                "444853000000": 'DHS',
                "504153495645": 'PASIVE',
            }
            for octet, name in names.items():
                expect(name).to(equal(octet2name(octet)))