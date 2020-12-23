from primestg.report import Report
from primestg.report.base import Concentrator

with description('Report instance'):
    with before.all:

        self.data_filenames = [
            'CIR4621247027_0_S02_0_20150901111051',
            'CIR4621247027_0_S02_0_20150901111051_warnings',
            'CIR4621247027_0_S04_0_20150901110412',
            'CIR4621247027_0_S04_0_20150901110412_warnings',
            'CIR4621247027_0_S05_0_20150901072044',
            'CIR4621247027_0_S05_0_20150901072044_warnings',
            'CIR4621802303_4F39_S05_0_20190221014548',
            'CIR4621247027_0_S12_0_20150903140000',
            'ZIV0000034180_0_S09_0_20161216104003',
            'ZIV0000034180_0_S09_0_20161216090401',
            'ZIV0000034180_0_S09_0_20161216080308',
            'ZIV0000035536_0_S15_0_20161204040002',
            'ZIV0000035545_0_S15_0_20161203040002',
            'ZIV0004311822_0_S15_0_20161215040002',
            'ZIV0000034180_0_S13_0_20161216080308',
            'ZIV0000034180_0_S13_0_20161216090401',
            'ZIV0000034180_0_S13_0_20161216104003',
            'ZIV0000035536_0_S17_0_20161204040002',
            'ZIV0000035545_0_S17_0_20161203040002',
            'ZIV0004311822_0_S17_0_20161215040002',
            'ZIV0004488684_59412C2_S23_0_20190424225341',
            'CIR4621816077_59864AC_S23_0_20190514165558'
        ]
    with it('Load a correct report without error'):
        for filename in self.data_filenames:
            with open('spec/data/' + filename) as data_file:
                message_tg = Report(data_file)
