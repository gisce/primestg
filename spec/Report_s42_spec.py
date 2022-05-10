from expects import expect, equal
from primestg.report import Report

with description('Report S42 type get example'):
    with before.all:
        self.data_filename = 'spec/data/CIR4621739284_71ED_S42_0_20220401080611'
        self.concentrators_name = 'CIR4621739284'
        self.report = {}
        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('Test integration file'):
        expect(self.report.concentrators[0].name).to(equal(self.concentrators_name))
        expect(len(self.report.values)).to(equal(4))
        first_item = self.report.concentrators[0].meters[0].values[0]
        expect(len(first_item)).to(equal(9))
        data_first_item = {'cnc_name': 'CIR4621739284',
                           'result': 'long_unsigned{6000}',
                           'name': 'CIR0502023221',
                           'Fh': '2022-04-01 08:06:08',
                           'Operation': 'get',
                           'obis': '1.0.0.4.2.255',
                           'data': '',
                           'class': '1',
                           'element': '2'}
        expect(first_item).to(equal(data_first_item))

with description('Report S42 type set example'):
    with before.all:
        self.data_filename = 'spec/data/CIR4621407021_31985_S42_0_20211213100140'
        self.concentrators_name = 'CIR4621407021'
        self.report = {}
        with open(self.data_filename) as data_file:
            self.report = Report(data_file)

    with it('Test integration file'):
        expect(self.report.concentrators[0].name).to(equal(self.concentrators_name))
        expect(len(self.report.values)).to(equal(8))
        first_item = self.report.concentrators[0].meters[0].values[0]
        expect(len(first_item)).to(equal(9))
        data_first_item = {'cnc_name': 'CIR4621407021',
                           'result': 'SUCCESS',
                           'name': 'ITE0131751928',
                           'Fh': '2021-12-13 10:01:09',
                           'Operation': 'set',
                           'obis': '0.1.94.34.11.255',
                           'data': 'raw{060000157c}',
                           'class': '3',
                           'element': '2'}
        expect(first_item).to(equal(data_first_item))
