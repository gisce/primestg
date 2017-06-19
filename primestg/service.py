# -*- coding: UTF-8 -*-

from zeep import Client


class Service(object):
    def __init__(self):
        self.DC_service = self.create_service()
        self.result = {}

    def send(self, report_id, meters, date_from, date_to):
        # TODO: need tocheck which report to demand and which parameters to send
        results = self.DC_service.Request(0002, report_id, date_from,
                                          date_to, meters, 2)

        return results

    def create_service(self):
        binding = 'XXXXXX'
        client = Client(
            wsdl='XXXXX')
        client.set_ns_prefix(None, 'XXXXX')
        return client.create_service(binding, 'XXXXX')

    def get_daily_incremental(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S02 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S02', meters, date_from, date_to)

    def get_all_daily_incremental(self, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S02 report for the corresponding meters
        """
        return self.send('S02', '', date_from, date_to)

    def get_monthly_billing(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S04 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S04', meters, date_from, date_to)

    def get_all_monthly_billing(self, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S04 report for the corresponding meters
        """
        return self.send('S04', '', date_from, date_to)

    def get_daily_absolute(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S05 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S05', meters, date_from, date_to)

    def get_meter_events(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S09 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S09', meters, date_from, date_to)

    def get_meter_parameters(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S06 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S06', meters, date_from, date_to)