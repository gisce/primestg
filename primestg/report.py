from datetime import datetime


class Measure(object):
    """
    Base class for a set of measures.
    """

    def __init__(self, measure):
        """
        Create a Measure object.

        :param measure: an lxml.objectify.StringElement representing a measure
        :return: a Measure object
        """
        self.measure = measure

    @property
    def measure(self):
        """
        The set of measures as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a measure
        """
        return self._measure

    @measure.setter
    def measure(self, value):
        """
        Stores the set of measures.

        :param value: an lxml.objectify.StringElement representing a measure
        :return:
        """
        self._measure = value

    def _get_timestamp(self, measure_name):
        """
        Formats the timestamp from a measure name

        :param measure_name: the measure name
        :return: a formatted string representing a timestamp \
            ('%Y-%m-%d %H:%M:%S')
        """
        value = self.measure.get(measure_name)
        if len(value) > 15:
            date_value = value[0:14] + value[-1]
        else:
            date_value = value

        # Fix for SAGECOM which puts this timestamp when the period doesn't
        # affect the contracted tariff
        if date_value.upper() == 'FFFFFFFFFFFFFFW':
            date_value = '19000101000000W'

        time = datetime.strptime(date_value[:-1], '%Y%m%d%H%M%S')
        return time.strftime('%Y-%m-%d %H:%M:%S')


class MeasureActiveReactive(Measure):
    """
    Base class for a set of measures with active and reactive measures.
    """

    def active_reactive(self, measure, measure_type):
        """
        Get the active and reactive measures.

        :param measure: an lxml.objectify.StringElement representing a set of \
            measures
        :param measure_type: the type of measure, added at the end of the \
            name of each measure ('a' or 'i')
        :return: a dict with the active and reactive measures
        """
        return {
            'ai': int(measure.get('AI{}'.format(measure_type))),
            'ae': int(measure.get('AE{}'.format(measure_type))),
            'r1': int(measure.get('R1{}'.format(measure_type))),
            'r2': int(measure.get('R2{}'.format(measure_type))),
            'r3': int(measure.get('R3{}'.format(measure_type))),
            'r4': int(measure.get('R4{}'.format(measure_type))),
        }


class MeasureS02(MeasureActiveReactive):
    """
    Class for a set of measures of report S02.
    """

    @property
    def value(self):
        """
        Set of measures of report S02.

        :return: a dict with a set of measures of report S02
        """
        value = self.active_reactive(self.measure, '')
        value.update(
            {
                'timestamp': self._get_timestamp('Fh'),
                'season': self.measure.get('Fh')[-1:],
                'bc': self.measure.get('Bc')
            }
        )
        return value


class Meter(object):
    """
    Base class for a meter.
    """

    def __init__(self, meter):
        """
        Create a Meter object.

        :param meter: an lxml.objectify.StringElement representing a meter
        :return: a Meter object
        """
        self.meter = meter

    @property
    def meter(self):
        """
        A meter as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a meter
        """
        return self._meter

    @meter.setter
    def meter(self, value):
        """
        Stores an lxml.objectify.StringElement representing a meter

        :param value: an lxml.objectify.StringElement representing a meter
        """
        self._meter = value

    @property
    def errors(self):
        """
        The meter errors.

        :return: a dict with the meter errors
        """
        self._errors = {}
        if self.meter.get('ErrCat'):
            self._errors = {
                'errcat': self.meter.get('ErrCat'),
                'errcode': self.meter.get('ErrCode')
            }
        return self._errors

    @property
    def name(self):
        """
        The name of the meter.

        :return: a string with the name of the meter
        """
        return self.meter.get('Id')

    @property
    def multiplier(self):
        """
        The multiplier of the meter measures.

        :return: a int with the multiplier of the meter measures
        """
        return self.meter.get('Magn')

    @property
    def report_type(self):
        """
        The type of report. To implement in child classes.
        """
        raise NotImplementedError('This method is not implemented!')

    @property
    def measure_class(self):
        """
        The class to instance measures sets.

        :return: a class to instance measure sets
        """
        return Measure

    @property
    def measure(self):
        """
        Measure set objects of this meter.

        :return: a list of measure set objects
        """
        measures = []
        if hasattr(self.meter, self.report_type):
            for measure in getattr(self.meter, self.report_type):
                measures.append(self.measure_class(measure))
        return measures

    @property
    def values(self):
        """
        Values of measure sets of this meter.

        :return: a list with de values of the measure sets
        """
        values = []
        for value in self.measure:
            values.append(value.value())
        return values


class MeterS02(Meter):
    """
    Class for a meter of report S02.
    """

    @property
    def report_type(self):
        """
        The type of report for report S02.

        :return: a string with 'S02'
        """
        return 'S02'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S02.

        :return: a class to instance measure sets of report S02
        """
        return MeasureS02

    @property
    def values(self):
        """
        Values of measure sets of this meter of report S02, with the name of \
            meter and the multiplier.

        :return: a list with de values of the measure sets
        """
        values = []
        for measure in self.measure:
            v = measure.value.copy()
            v['name'] = self.name
            v['magn'] = int(self.multiplier)
            values.append(v)
        if values:
            return values
        else:
            return {}


class Concentrator(object):
    """
    Base class for a concentrator.
    """

    def __init__(self, concentrator):
        """
        Create a Concentrator object.

        :param concentrator: an lxml.objectify.StringElement representing a \
            concentrator
        :return: a Concentrator object
        """
        self.concentrator = concentrator

    @property
    def concentrator(self):
        """
        A concentrator as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a concentrator
        """
        return self._concentrator

    @concentrator.setter
    def concentrator(self, value):
        """
        Stores a concentrator as an lxml.objectify.StringElement.

        :param value: an lxml.objectify.StringElement representing a \
            concentrator
        """
        self._concentrator = value

    @property
    def meter_class(self):
        """
        The class to instance meters.

        :return: a class to instance meters
        """
        return Meter

    @property
    def meter(self):
        """
        Meter objects of this concentrator.

        :return: a list of meter objects
        """
        meters = []
        for meter in self.concentrator.Cnt:
            meters.append(self.meter_class(meter))
        return meters

    @property
    def name(self):
        """
        The name of the concentrator.

        :return: a string with the name of the concentrator
        """
        return self.concentrator.get('Id')

    @property
    def values(self):
        """
        Values of the meters of this concentrator.

        :return: a list with de values of the meters
        """
        values = []
        for meter in self.meter:
            values.append(meter.values)
        return values


class ConcentratorS02(Concentrator):
    """
    Class for a concentrator of report S02.
    """

    @property
    def meter_class(self):
        """
         The class used to instance meters for report S02.

        :return: a class to instance meters of report S02
        """
        return MeterS02


class Report(object):
    """
    Report class to process MessageS
    """

    def __init__(self, message):
        """
        Creates a Report object.

        :param message: a MessageS object
        :return: an Report object
        """
        self.message = message

    @property
    def message(self):
        """
        A message as a MessageS.

        :return: a MessageS object
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        Stores the message as a MessageS.

        :param value: a MessageS object
        """
        self._message = value

    @property
    def report_type(self):
        """
        The report type.

        :return: a string with the report type
        """
        return self.message.objectified.get('IdRpt')

    @property
    def concentrator_class(self):
        if self.report_type == 'S02':
            concentrator_class = ConcentratorS02
        else:
            raise NotImplementedError('Report type not implemented!')
        return concentrator_class

    @property
    def concentrator(self):
        """
        The concentrators of the report.

        :return: a list of concentrators of the report
        """
        concentrators = []
        for concentrator in self.message.objectified.Cnc:
            concentrators.append(self.concentrator_class(concentrator))
        return concentrators

    @property
    def values(self):
        """
        Values of the whole report.

        :return: a list with the values of the whole report
        """
        values = []
        for concentrator in self.concentrator:
            values.extend(concentrator.values)
        return values