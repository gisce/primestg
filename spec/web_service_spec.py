from expects import expect, equal
from primestg.report import Report
import responses
import requests
from primestg.service import Service
from zeep.transports import Transport

with description('Web services run'):
    with before.all:
        self.s = Service()

    with it('asking for S02 report'):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'http://cct.gisce.lan:8080/',
                     body='{}', status=200,
                     content_type='application/json')

            resp = self.s.get_daily_incremental('ZIV0040318130',
                                                '20170610010000',
                                                '20170611000000')

            assert resp.json() == {"error": "not found"}
