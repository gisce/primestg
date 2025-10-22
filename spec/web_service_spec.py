import responses
import primestg
from primestg.service import Service
from zeep.exceptions import TransportError

with description('Web services run'):
    with before.all:
        # Only if NDA wsdl available
        if not primestg.get_data('WS_DC.wsdl'):
            exit(0)
        self.s = Service(1, 'http://cct.gisce.lan:8080/')

    with it('asking for S02 report with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S02 error"}', status=404)
            try:
                resp = self.s.get_daily_incremental('ZIV0040318130',
                                                    '20170610010000',
                                                    '20170611000000')
            except TransportError as te:
                assert 'expected S02 error' in te.message

    with it('asking for S02 report for all meters with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S02 error"}', status=404)
            try:
                resp = self.s.get_all_daily_incremental('20170610010000',
                                                        '20170611000000')
            except TransportError as te:
                assert 'expected S02 error' in te.message

    with it('asking for S04 report with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S04 error"}', status=404)
            try:
                resp = self.s.get_monthly_billing('ZIV0040318130',
                                                  '20170600010000',
                                                  '20170631000000')
            except TransportError as te:
                assert 'expected S04 error' in te.message

    with it('asking for S04 report for all meters with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S04 error"}', status=404)
            try:
                resp = self.s.get_all_monthly_billing('20170600010000',
                                                      '20170631000000')
            except TransportError as te:
                assert 'expected S04 error' in te.message

    with it('asking for S05 report with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S05 error"}', status=404)
            try:
                resp = self.s.get_daily_absolute('ZIV0040318130',
                                                 '20170609010000',
                                                 '20170611000000')
            except TransportError as te:
                assert 'expected S05 error' in te.message

    with it('asking for S05 report for all meters with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S05 error"}', status=404)
            try:
                resp = self.s.get_all_daily_absolute('20170609010000',
                                                     '20170611000000')
            except TransportError as te:
                assert 'expected S05 error' in te.message

    with it('asking for S09 report with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S09 error"}', status=404)
            try:
                resp = self.s.get_meter_events('ZIV0040318130',
                                               '20170609010000',
                                               '20170611000000',
                                               'EvGroup:;EvCode:')
            except TransportError as te:
                assert 'expected S09 error' in te.message

    with it('asking for S06 report with mocked connection'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{"error": "expected S06 error"}', status=404)
            try:
                resp = self.s.get_meter_parameters('ZIV0040318130',
                                                   '20170609010000',
                                                   '20170611000000')
            except TransportError as te:
                assert 'expected S06 error' in te.message
