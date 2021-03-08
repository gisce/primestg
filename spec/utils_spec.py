# -*- coding: utf-8 -*-
from expects import expect, raise_error, be_a, equal
from primestg.utils import DLMSTemplates, ContractTemplates, datetohexprime
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