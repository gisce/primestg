from datetime import datetime


MAGNITUDE_W = 1
"""
Magnitude value (1) for measures represented in W.
"""

MAGNITUDE_KW = 1000
"""
Magnitude value (1000) for measures represented in kW.
"""


class ValueWithTime(object):
    """
    Base class for values with time.
    """

    def _get_timestamp(self, name, element=None):
        """
        Formats a timestamp from the name of the value.

        :param name: a string with the name
        :param element: an lxml.objectify.StringElement, by default \
            self.objectified
        :return: a formatted string representing a timestamp \
            ('%Y-%m-%d %H:%M:%S')
        """
        if element is None:
            e = self.objectified
        else:
            e = element
        value = e.get(name)
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


class Measure(ValueWithTime):
    """
    Base class for a set of measures.
    """

    def __init__(self, objectified_measure):
        """
        Create a Measure object.

        :param objectified_measure: an lxml.objectify.StringElement \
            representing a set of measures
        :return: a Measure object
        """
        self.objectified = objectified_measure

    @property
    def objectified(self):
        """
        The set of measures as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a set of measures
        """
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Stores an lxml.objectify.StringElement representing a set of measures.

        :param value: an lxml.objectify.StringElement representing a set of \
            measures
        :return:
        """
        self._objectified = value


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


class Parameter(ValueWithTime):
    """
    Base class for a set of parameters.
    """

    def __init__(self, objectified_parameter, report_version):
        """
        Create a Parameter object.

        :param objectified_parameter: an lxml.objectify.StringElement \
            representing a set of parameters
        :return: a Measure object
        """
        self.objectified = objectified_parameter
        self.report_version = report_version

    @property
    def objectified(self):
        """
        The set of parameters as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a set of \
            parameters
        """
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Stores an lxml.objectify.StringElement representing a set of \
            parameters.

        :param value: an lxml.objectify.StringElement representing a set of \
            parameters
        :return:
        """
        self._objectified = value

    @property
    def report_version(self):
        """
        The version of the report.

        :return: a string with the version of the report
        """
        return self._report_version

    @report_version.setter
    def report_version(self, value):
        """
        Stores the report version.
        :param value: a string with the version of the report
        """
        self._report_version = value

    def get_boolean(self, name, element=None):
        """
        Gets a boolean value from the name of value.

        :param name: a string with the name
        :param element: an lxml.objectify.StringElement, by default \
            self.objectified
        :return:
        """
        if element is None:
            e = self.objectified
        else:
            e = element
        if e.get(name) == 'Y':
            returns = True
        else:
            returns = False
        return returns

    def to_integer(self, value):
        """
        Convert a value to an integer. If value is None then returns 0.

        :param value: a string with the value
        :return: an integer
        """
        if value is None:
            returns = 0
        else:
            returns = int(value)
        return returns

    def filter_integer(self, value):
        """
        Filter the provided value. Returns the value if is an integer or \
            returns 0 if not.

        :param value: an integer or not
        :return: an integer
        """
        if isinstance(value, int):
            returns = value
        else:
            returns = 0
        return returns

    @property
    def values(self):
        """
        Set of parameters.
        """
        raise NotImplementedError('This method is not implemented!')


class Meter(object):
    """
    Base class for a meter.
    """

    def __init__(self, objectified_meter):
        """
        Create a Meter object.

        :param objectified_meter: an lxml.objectify.StringElement \
            representing a meter
        :return: a Meter object
        """
        self.objectified = objectified_meter

    @property
    def objectified(self):
        """
        A meter as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a meter
        """
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Stores an lxml.objectify.StringElement representing a meter

        :param value: an lxml.objectify.StringElement representing a meter
        """
        self._objectified = value

    @property
    def errors(self):
        """
        The meter errors.

        :return: a dict with the meter errors
        """
        self._errors = {}
        if self.objectified.get('ErrCat'):
            self._errors = {
                'errcat': self.objectified.get('ErrCat'),
                'errcode': self.objectified.get('ErrCode')
            }
        return self._errors

    @property
    def name(self):
        """
        The name of the meter.

        :return: a string with the name of the meter
        """
        return self.objectified.get('Id')

    @property
    def magnitude(self):
        """
        The magnitude of the meter measures.

        :return: a int with the magnitude of the meter measures
        """
        return int(self.objectified.get('Magn'))

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
    def measures(self):
        """
        Measure set objects of this meter.

        :return: a list of measure set objects
        """
        measures = []
        if hasattr(self.objectified, self.report_type):
            objectified = getattr(self.objectified, self.report_type)
            measures = map(self.measure_class, objectified)
        return measures

    @property
    def values(self):
        """
        Values of measure sets of this meter.

        :return: a list with the values of the measure sets
        """
        values = []
        for measure in self.measures:
            values.append(measure.value())
        return values


class MeterWithConcentratorName(Meter):
    """
    Base class for a meters of report that need the name of the concentrator \
        in the values, like S04 and S05.
    """

    def report_type(self):
        """
        The type of report. To implement in child classes.
        """
        raise NotImplementedError('This method is not implemented!')

    def __init__(self, objectified_meter, concentrator_name):
        """
        Create a Meter object using Meter constructor and adding the \
            concentrator name.

        :param objectified_meter: an lxml.objectify.StringElement \
            representing a meter
        :param concentrator_name: a string with the name of the concentrator
        :return: a Meter object
        """
        super(MeterWithConcentratorName, self).__init__(objectified_meter)
        self.concentrator_name = concentrator_name

    @property
    def concentrator_name(self):
        """
        A string with the concentrator name.

        :return: a string with the concentrator name
        """
        return self._concentrator_name

    @concentrator_name.setter
    def concentrator_name(self, value):
        """
        Stores a string with the concentrator name.

        :param value: a string with the concentrator name
        """
        self._concentrator_name = value

    @property
    def values(self):
        """
        Values of measure sets of this meter of report that need the name of \
            the concentrator and the meter,

        :return: a list with the values of the measure sets
        """
        values = []
        for measure in self.measures:
            for subvalue in measure.values:
                v = subvalue.copy()
                v['name'] = self.name
                v['cnc_name'] = self.concentrator_name
                values.append(v)
        return values

class Concentrator(object):
    """
    Base class for a concentrator.
    """

    def __init__(self, objectified_concentrator):
        """
        Create a Concentrator object.

        :param objectified_concentrator: an lxml.objectify.StringElement \
            representing a concentrator
        :return: a Concentrator object
        """
        self.objectified = objectified_concentrator

    @property
    def objectified(self):
        """
        A concentrator as an lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement representing a concentrator
        """
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Stores a concentrator as an lxml.objectify.StringElement.

        :param value: an lxml.objectify.StringElement representing a \
            concentrator
        """
        self._objectified = value

    @property
    def meter_class(self):
        """
        The class to instance meters.

        :return: a class to instance meters
        """
        return Meter

    @property
    def meters(self):
        """
        Meter objects of this concentrator.

        :return: a list of meter objects
        """
        return map(self.meter_class, self.objectified.Cnt)

    @property
    def name(self):
        """
        The name of the concentrator.

        :return: a string with the name of the concentrator
        """
        return self.objectified.get('Id')

    @property
    def values(self):
        """
        Values of the meters of this concentrator.

        :return: a list with the values of the meters
        """
        values = []
        for meter in self.meters:
            values.extend(meter.values)
        return values


class ConcentratorWithMetersWithConcentratorName(Concentrator):
    """
    Base class for a concentrator of report that need the name of the \
        concentrator in the values, like S04 and S05.
    """

    @property
    def meters(self):
        """
        Meter objects of this concentrator. The name of concentrator is \
            passed to the meter.

        :return: a list of meter objects
        """
        meters = []
        for meter in self.objectified.Cnt:
            meters.append(self.meter_class(meter, self.name))
        return meters
