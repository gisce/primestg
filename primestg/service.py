# -*- coding: UTF-8 -*-

from zeep import Client
from requests import Session
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
import xml.etree.ElementTree as ET


class Service(object):
    def __init__(self):
        self.DC_service = self.create_service()
        self.result = {}

    def send(self, report_id, meters, date_from, date_to):
        # crida als webservices segons els parametres que em passin,
        # que seran els del metode concret de cada report
        results = self.DC_service.Request(0002, report_id, date_from,
                                               date_to, meters, 2)
        # for rep_res in results:
        # root = ET.fromstring(results)
        # print '=========================================='
        # print(ET.tostring(root))
        # print '=========================================='
        return results

    def create_service(self):
        binding = '{http://www.asais.fr/ns/Saturne/DC/ws}WS_DCSoap'
        client = Client(
            wsdl='/home/miquel/codi/primestg/primestg/data/WS_DC.wsdl')
        client.set_ns_prefix(None, 'http://www.asais.fr/ns/Saturne/DC/ws')
        return client.create_service(binding, 'http://cct.gisce.lan:8080')

    def get_daily_incremental(self, meters, date_from, date_to):
        """
        If meter is empty list do it for all meters.
        :param meters: either meter_id, list of meter_id's or empty list
        :return: an S02 report for the corresponding meters
        """
        if isinstance(meters, list):
            meters = ','.join(meters)
        return self.send('S02', meters, date_from, date_to)
