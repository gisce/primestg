from expects import expect, equal
from primestg.report import Report
from ast import literal_eval

with description('Report G04 example'):
    with before.all:

        data_filename = 'spec/data/CIR4621511370_0_G04_0_20260922081142'
        with open(data_filename) as data_file:
            self.report = Report(data_file)

    with it('generates result with the expected fields'):

        first_value_meter = {
            'timestamp': '2026-09-15 04:00:00',
            'season': 'S',
            'i1_lv': 122.9,
            'i2_lv': 115.9,
            'i3_lv': 126.1,
            'ineutral': 10.7,
            'v1_lv': 137,
            'v2_lv': 137,
            'v3_lv': 137,
            'v1_mv': 11368,
            'v2_mv': 11366,
            'v3_mv': 11344,
            'ai': 46290,
            'ae': 0,
            'r_inductiva': 8300,
            'r_capacitiva': 2820,
            'v1_comp': 137,
            'v2_comp': 2,
            'vo_comp': 2,
            'v_hs': 0,
            'bc': '82',
            'name': 'CIR2081429002',
            'cnc_name': 'CIR4621511370'
        }
        concentrator = list(self.report.concentrators)[0]
        parameter = concentrator.meters[0]
        first_value = parameter.values[0]
        expect(first_value).to(equal(first_value_meter))
