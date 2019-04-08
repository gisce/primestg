# -*- coding: UTF-8 -*-

from zeep import Client
import primestg
from datetime import datetime
import calendar


B11_TEMPLATE = """<Order IdPet="{idpet}" IdReq="B11" Version="3.1.c">
    <Cnc Id="{cnc_id}">
        <B11 Order="{order}" Args="" Fini="{start_date}" Ffin="{end_date}">
        </B11>
    </Cnc>
</Order>
"""


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

    def order(self, cnc_id, order, start_date=None, end_date=None):
        """
        :param cnc_id: Id concentrador
        :type cnc_id: str
        :param order: Tipo de order (T01, T02, T03, T04, ...)
        :type order: str
        :param start_date: Fecha inicio, si está vacio coge ahora)
        :type start_date: datetime
        :param end_date: Fecha final, si está vacio coge ahora)
        :type end_date: datetime
        :return: Resultado petición
        :rtype: bool
        """

        if start_date is None:
            start_date = datetime.now()
        if end_date is None:
            end_date = datetime.now()

        b11 = B11_TEMPLATE.format(
            idpet=self.fact_id,
            cnc_id=cnc_id,
            order=order,
            start_date=format_timestamp(start_date),
            end_date=format_timestamp(end_date)
        )
        return self.DC_service.Order(self.fact_id, 0, b11, 3)

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
        return self.send('S01', meters)

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
