# -*- coding: UTF-8 -*-

from zeep import Client
import primestg


class Service(object):
    def __init__(self, fact_id, cnc_url, sync=True, source=None):
        self.cnc_url = cnc_url
        self.fact_id = fact_id
        self.sync = sync
        if not source:
            self.source = 'DCF'  # By default it doesn't look to the meter for data
        else:
            self.source = source
        self.DC_service = self.create_service()

    def send(self, report_id, meters, date_from='', date_to=''):

        if self.sync:
            results = self.DC_service.Request(self.fact_id, report_id,
                                              date_from, date_to, meters, 2)
        else:
            results = self.DC_service.AsynchRequest(self.fact_id, report_id,
                                                    date_from, date_to,
                                                    meters, 2, self.source)

        return results

    def create_service(self):
        binding = '{http://www.asais.fr/ns/Saturne/DC/ws}WS_DCSoap'
        client = Client(wsdl=primestg.get_data('WS_DC.wsdl'))
        client.set_ns_prefix(None, 'http://www.asais.fr/ns/Saturne/DC/ws')
        return client.create_service(binding, self.cnc_url)

    def get_instant_data(self, meters):
        """
        Asks for a S01 report to the specified meter.
        :param meters: a meter_id
        :return: an S01 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S01', meters)

    def get_daily_incremental(self, meters, date_from, date_to):
        """
        Asks for a S02 report to the specified meter.
        :param meters: a meter_id
        :return: an S02 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S02', meters, date_from, date_to)

    def get_all_daily_incremental(self, date_from, date_to):
        """
        Asks for a S02 report to all meters.
        :return: an S02 report from every meter
        """
        return self.send('S02', '', date_from, date_to)

    def get_monthly_billing(self, meters, date_from, date_to):
        """
        Asks for a S04 report to the specified meter.
        :param meters: a meter_id
        :return: an S04 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S04', meters, date_from, date_to)

    def get_all_monthly_billing(self, date_from, date_to):
        """
        Asks for a S04 report to all meters.
        :return: an S04 report from every meter
        """
        return self.send('S04', '', date_from, date_to)

    def get_daily_absolute(self, meters, date_from, date_to):
        """
        Asks for a S05 report to the specified meter.
        :param meters: a meter_id
        :return: an S05 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S05', meters, date_from, date_to)

    def get_all_daily_absolute(self, date_from, date_to):
        """
        Asks for a S05 report to all meters.
        :return: an S05 report from every meter
        """
        return self.send('S05', '', date_from, date_to)

    def get_meter_events(self, meters, date_from, date_to):
        """
        Asks for a S09 report to the specified meter.
        :param meters: a meter_id
        :return: an S09 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S09', meters, date_from, date_to)

    def get_all_meter_events(self, date_from, date_to):
        """
        Asks for a S09 report to all meters.
        :return: an S09 report from every meter
        """
        return self.send('S09', '', date_from, date_to)

    def get_meter_parameters(self, meters, date_from, date_to):
        """
        Asks for a S06 report to the specified meter.
        :param meters: a meter_id
        :return: an S06 report for the corresponding meter
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S06', meters, date_from, date_to)

    def get_all_meter_parameters(self, date_from, date_to):
        """
        Asks for a S06 report to all meters.
        :return: an S06 report from every meter
        """
        return self.send('S06', '', date_from, date_to)

    def get_concentrator_parameters(self, dc, date_from, date_to):
        """
        Asks for a S12 report to the concentrator.
        :return: an S12 report from the concentrator.
        """
        return self.send('S12', dc, date_from, date_to)
