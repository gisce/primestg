# -*- coding: UTF-8 -*-
from zeep import Client
from zeep.transports import Transport
from datetime import datetime
import primestg
from primestg.order.orders import Order
import calendar
from .utils import PRIORITY_HIGH


def last_sunday(year, month):
    """Retorna l'últim diumenge del mes, serveix per determinar quin dia
    s'ha de canviar l'hora.
    """
    for day in reversed(range(1, calendar.monthrange(year, month)[1] + 1)):
        if calendar.weekday(year, month, day) == calendar.SUNDAY:
            return datetime(year, month, day)


def format_timestamp(dt):
    """Returns format "YYYYMMDDHHMNSSFFFX"

    :param dt: Datetime to parse
    :type dt: datetime
    :return: timestamp string
    :rtype: str
    """
    march = last_sunday(dt.year, 3).replace(hour=2)
    october = last_sunday(dt.year, 10).replace(hour=2)
    if march < dt < october:
        season = 'S'
    else:
        season = 'W'
    return '{}{}'.format(dt.strftime('%Y%m%d%H%M%S000'), season)


class Service(object):
    def __init__(self, fact_id, cnc_url, sync=True, source=None, priority=None):
        self.cnc_url = cnc_url
        self.fact_id = fact_id
        self.sync = sync
        if not priority:
            self.priority = PRIORITY_HIGH
        else:
            self.priority = priority

        if not source:
            self.source = 'DCF'  # By default it doesn't look to the meter for data
        else:
            self.source = source

        self.DC_service = self.create_service()

    def send(self, report_id, meters, date_from='', date_to='', priority=None):
        if priority is None:
            priority = self.priority

        if self.sync:
            results = self.DC_service.Request(self.fact_id, report_id,
                                              date_from, date_to, meters, priority)
        else:
            results = self.DC_service.AsynchRequest(self.fact_id, report_id,
                                                    date_from, date_to,
                                                    meters, priority, self.source)
        return results

    def send_order(self, report_id, order, priority=None):
        """
        Sends order
        :param report_id: B11,B09,etc.
        :param order: XML containing order
        :param priority: default PRIORITY_HIGHEST,
        :return: true or false
        """
        if priority is None:
            priority = self.priority
        print(order)
        results = self.DC_service.Order(self.fact_id, 0, order, priority)
        return results

    def get_powers(self, generic_values, payload):
        """
        Sends B02 order to meter
        :return: Success or fail
        """
        order = Order('B02')
        order = order.create(generic_values, payload)
        return self.send_order('B02', order)

    def get_cutoff_reconnection(self, generic_values, payload):
        """
        Sends B03 order to meter
        :return: Success or fail
        """
        order = Order('B03')
        order = order.create(generic_values, payload)
        return self.send_order('B03', order)

    def get_contract(self, generic_values, payload):
        """
        Sends B03 order to meter
        :return: Success or fail
        """
        order = Order('B04')
        order = order.create(generic_values, payload)
        return self.send_order('B04', order)

    def get_concentrator_modification(self, generic_values, payload):
        """
        Sends B07 order to meter
        :return: Success or fail
        """
        order = Order('B07')
        order = order.create(generic_values, payload)
        return self.send_order('B07', order)

    def set_concentrator_ip(self, generic_values, payload):
        order = Order('B07_ip')
        order = order.create(generic_values, payload)
        return self.send_order('B07', order)

    def get_meter_modification(self, generic_values, payload):
        """
        Sends B09 order to meter
        :return: Success or fail
        """
        order = Order('B09')
        order = order.create(generic_values, payload)
        return self.send_order('B09', order)

    def get_order_request(self, generic_values, payload):
        """
        Sends B11 order to concentrator
        :return: Success or fail
        """
        order = Order('B11')
        order = order.create(generic_values, payload)
        return self.send_order('B11', order)

    def order_raw_dlms(self, generic_values, payload):
        """
        Sends B12 order to concentrator
        :return: Success or fail
        """
        order = Order('B12')
        order = order.create(generic_values, payload)
        return self.send_order('B12', order)

    def create_service(self):
        transport = Transport(timeout=20, operation_timeout=60)
        binding = '{http://www.asais.fr/ns/Saturne/DC/ws}WS_DCSoap'
        client = Client(wsdl=primestg.get_data('WS_DC.wsdl'), transport=transport)
        client.set_ns_prefix(None, 'http://www.asais.fr/ns/Saturne/DC/ws')
        return client.create_service(binding, self.cnc_url)

    def get_instant_data(self, meters):
        """
        Asks for a S01 report to the specified meter.
        :param meters: a meter_id
        :return: an S01 report for the corresponding meter
        """
        return self.send('S01', meters)

    def get_advanced_instant_data(self, meters):
        """
        Asks for a S21 report to the specified meter.
        :param meters: a meter_id
        :return: an S21 report for the corresponding meter
        """
        return self.send('S21', meters)

    def get_contract_definition(self, meters, date_from, date_to):
        """
        Asks for a S23 report to the specified meter.
        :param meters: a meter_id
        :return: an S23 report for the corresponding meter
        """
        return self.send('S23', meters, date_from, date_to)

    def get_all_contract_definition(self, date_from, date_to):
        """
        Asks for a S23 report to all meters.
        :return: an S23 report from every meter
        """
        return self.send('S23', '', date_from, date_to)

    def get_daily_incremental(self, meters, date_from, date_to):
        """
        Asks for a S02 report to the specified meter.
        :param meters: a meter_id
        :return: an S02 report for the corresponding meter
        """
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

    def get_daily_average_voltage_and_current(self, meters, date_from, date_to):
        """
        Asks for a S14 report to the specified meter.
        :param meters: a meter_id
        :return: an S14 report for the corresponding meter
        """
        return self.send('S14', meters, date_from, date_to)

    def get_all_daily_average_voltage_and_current(self, date_from, date_to):
        """
        Asks for a S14 report to all meters.
        :return: an S14 report from every meter
        """
        return self.send('S14', '', date_from, date_to)

    def get_concentrator_events(self, dc, date_from, date_to):
        """
        Asks for a S17 report to the concentrator.
        :return: an S17 report from the concentrator.
        """
        return self.send('S17', dc, date_from, date_to)

    def get_cutoffs_status(self, meters, date_from, date_to):
        """
        Asks for a S18 report to the specified meter.
        :param meters: a meter_id
        :return: an S18 report for the corresponding meter
        """
        return self.send('S18', meters, date_from, date_to)

    def get_all_cutoffs_status(self, date_from, date_to):
        """
        Asks for a S18 report to all meters.
        :return: an S18 report from every meter
        """
        return self.send('S18', '', date_from, date_to)

    def get_all_contract_definition(self, date_from, date_to):
        """
        Asks for a S23 report to all meters.
        :return: an S23 report from every meter
        """
        return self.send('S23', '', date_from, date_to)

    def get_concentrator_meters(self, dc, date_from, date_to):
        """
        Asks for a S24 report to the concentrator.
        :return: an S24 report from the concentrator.
        """
        return self.send('S24', dc, date_from, date_to)

    def get_current_billing(self, meter, date_from, date_to):
        """
        Asks for a S27 report to the meter.
        :return: an S27 report from the meter.
        """
        return self.send('S27', meter, date_from, date_to)