# -*- coding: utf-8 -*-
from expects import expect, raise_error, be_a, equal, match
from primestg.utils import DLMSTemplates, ContractTemplates, datetohexprime, octet2name, name2octet, octet2date
from primestg.dlms_templates import DLMS_TEMPLATES
from datetime import date, datetime


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

    with context("octet2date"):
        with it("returns a date"):
            dates = {
                "07E504010400000": datetime(2021, 4, 1, 4, 0, 0),
                "07E5060102000000FF800080": datetime(2021, 6, 1, 2, 0, 0),
                "07E506010200000": datetime(2021, 6, 1, 2, 0, 0),
                "07E50601FF000000FF800009": datetime(2021, 6, 1, 0, 0, 0),
                "07E50601FF00009": datetime(2021, 6, 1, 0, 0, 0),
                "20140204110552000W": datetime(2014, 2, 4, 11, 5, 52),
                "20190102134203000W": datetime(2019, 1, 2, 13, 42, 3),
                "20210501000000000S": datetime(2021, 5, 1, 0, 0, 0),
                # special days
                "FFFF0101000000000W": datetime(9999, 1, 1, 0, 0, 0),
                "FFFF0106000000000W": datetime(9999, 1, 6, 0, 0, 0),
                "FFFF0501000000000W": datetime(9999, 5, 1, 0, 0, 0),
                "FFFF0815000000000W": datetime(9999, 8, 15, 0, 0, 0),
                "FFFF1012000000000W": datetime(9999, 10, 12, 0, 0, 0),
                "FFFF1101000000000W": datetime(9999, 11, 1, 0, 0, 0),
                "FFFF1206000000000W": datetime(9999, 12, 6, 0, 0, 0),
                "FFFF1208000000000W": datetime(9999, 12, 8, 0, 0, 0),
                "FFFF1225000000000W": datetime(9999, 12, 25, 0, 0, 0),
                #wrong month
                "21110021000000000W": datetime(2111, 1, 21, 0, 0, 0),
                # wrong year
                "00001228230000000W": "time data '0-12-28 23:0:0' does not match format '%Y-%m-%d %H:%M:%S'"
            }
            for octet, dt in dates.items():
                if isinstance(dt, (basestring)):
                    expect(lambda: octet2date(octet)).to(raise_error(ValueError, dt))
                else:
                    result_date = octet2date(octet)
                    expect(dt).to(equal(result_date))

