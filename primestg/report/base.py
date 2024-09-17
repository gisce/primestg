from datetime import datetime
import binascii
import re
from primestg.utils import octet2date


MAGNITUDE_W = 1
"""
Magnitude value (1) for measures represented in W.
"""

MAGNITUDE_KW = 1000
"""
Magnitude value (1000) for measures represented in kW.
"""

SAGE_BAD_TIMESTAMP = [
    'FFFFFFFFFFFFFFW',
    'FFFFFFFF000000S',
    '00150000000000W',
    '18070000000000W',
]

S23_BAD_TIMESTAMP = [
    '00000000000000S',
    '00000000000000W',
    '000000000000000',
    'FFFFFFFFFFFFFF9',
    'FFFFFFFFFFFFFF0',
    'FFFFFFFFFFFFFFF',
    'FFFFFFFFFFFFF79',
]

BAD_TIMESTAMP = SAGE_BAD_TIMESTAMP + S23_BAD_TIMESTAMP


DAYSAVING_START_TS = 'FFFFFDFFFFFFFF0000800000'   # Winter to summer
DAYSAVING_END_TS = 'FFFFFEFFFFFFFF0000800080'     # Summer to winter
NOW_ACTIVATION_DATE = 'FFFFFFFFFFFFFFFFFF800009'  # Instantly activate latent contract


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
        e = self.objectified if element is None else element

        return self._to_timestamp(e.get(name), name)

    @staticmethod
    def _to_timestamp(value, name):
        date_value = value[0:14] + value[-1] if len(value) > 15 else value

        # Fix for SAGECOM which puts this timestamp when the period doesn't affect the contracted tariff
        if date_value.upper() in BAD_TIMESTAMP or not date_value:
            date_value = '19010101000000W'

        try:
            time = octet2date(date_value)
        except ValueError as e:
            raise ValueError("Date out of range: {} ({}) {}".format(
                date_value, name, e))

        return time.strftime('%Y-%m-%d %H:%M:%S')

    def _get_special_days(self, name, element=None):
        """
        Formats a timestamp from the name of the value.

        :param name: a string with the name
        :param element: an lxml.objectify.StringElement, by default self.objectified
        :return: {
            timestamp: a formatted string representing a timestamp ('%Y-%m-%d %H:%M:%S')
            year: number|False,
            month: number,
            day: number
        }
        """
        e = self.objectified if element is None else element
        value = e.get(name)

        if not value:
            return None

        year = value[0:4]

        if e.get('DTCard') == 'Y':
            value = '9999' + value[4:]

        return {
            'year': int(year) if year.isdigit() else False,
            'month': int(value[4:6]),
            'day': int(value[6:8]),
            'timestamp': self._to_timestamp(value, name)
        }


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
        self._warnings = []

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

    @property
    def warnings(self):
        """
        Warnings of these measures.

        :return: a list with the errors found while reading
        """
        return self._warnings


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


class MeasureActiveReactiveFloat(Measure):
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
            'ai': float(measure.get('AI{}'.format(measure_type))),
            'ae': float(measure.get('AE{}'.format(measure_type))),
            'r1': float(measure.get('R1{}'.format(measure_type))),
            'r2': float(measure.get('R2{}'.format(measure_type))),
            'r3': float(measure.get('R3{}'.format(measure_type))),
            'r4': float(measure.get('R4{}'.format(measure_type))),
        }

    def active_reactive_with_phase(self, measure, phase_num):
        """
        Get the active and reactive measures.

        :param measure: an lxml.objectify.StringElement representing a set of \
            measures
        :param phase_num: the phase number of measure, added at the end of the \
            name of each measure (1,2,3)
        :return: a dict with the active and reactive phase measures
        """
        return {
            'ai{}'.format(phase_num): float(measure.get('AI{}'.format(phase_num))),
            'ae{}'.format(phase_num): float(measure.get('AE{}'.format(phase_num))),
            'r1{}'.format(phase_num): float(measure.get('R1{}'.format(phase_num))),
            'r2{}'.format(phase_num): float(measure.get('R2{}'.format(phase_num))),
            'r3{}'.format(phase_num): float(measure.get('R3{}'.format(phase_num))),
            'r4{}'.format(phase_num): float(measure.get('R4{}'.format(phase_num))),
        }


class MeasureAverageVoltageAndCurrent(Measure):
    """
    Base class for a set of measures with average voltage and current.
    """

    def average_voltage_and_current(self, measure):
        """
        Get the average voltage and current measures.

        :param measure: an lxml.objectify.StringElement representing a set of \
            measures
        :return: a dict with the active and reactive measures
        """
        return {
            'v1': float(measure.get('V1')),
            'v2': float(measure.get('V2')),
            'v3': float(measure.get('V3')),
            'i1': float(measure.get('I1')),
            'i2': float(measure.get('I2')),
            'i3': float(measure.get('I3')),
            'in': float(measure.get('In')),
        }


class Operation(Measure):
    """
    Base class for a meter operation.
    """
    pass


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
        self._warnings = []

    def meter_availability(self, meter):
        """
            Get meter availability.

            :param meter: an lxml.objectify.StringElement representing a the
            availability of the meter at a certain hour
            :return: a dict with the availability of the meter and hour
        """
        values = {}
        try:
            timestamp = self._get_timestamp('Date', element=meter)
            values = {
                'name': meter.get('MeterId'),
                'status': int(meter.get('ComStatus')),
                'timestamp': timestamp,
                'season': meter.get('Date')[-1:],
                'active': self.get_boolean('Active', element=meter),
            }
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
        return values

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

    @property
    def warnings(self):
        """
        Warnings of these parameters.

        :return: a list with the errors found while reading
        """
        return self._warnings


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
        self._warnings = {}

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

    @property
    def warnings(self):
        """
        Warnings of this meter.

        :return: a list with the errors found while reading
        """
        return self._warnings


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
            if measure.warnings:
                if self._warnings.get(self.name, False):
                    self._warnings[self.name].extend(measure.warnings)
                else:
                    self._warnings.update({self.name: measure.warnings})
        return values


class MeterWithMagnitude(MeterWithConcentratorName):

    @property
    def magnitude(self):
        """
        The magnitude of the meter measures.

        :return: a int with the magnitude of the meter measures
        """
        return int(self.objectified.get('Magn'))


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
        self._warnings = []

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
    def name(self):
        """
        The name of the concentrator.

        :return: a string with the name of the concentrator
        """
        return self.objectified.get('Id')

    @property
    def warnings(self):
        """
        Warnings of this concentrator.

        :return: a list with the errors found while reading
        """
        return self._warnings


class ConcentratorWithMeters(Concentrator):

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
    def values(self):
        """
        Values of the meters of this concentrator.

        :return: a list with the values of the meters
        """
        values = []
        for meter in self.meters:
            values.extend(meter.values)
        return values


class ConcentratorWithMetersWithConcentratorName(ConcentratorWithMeters):
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
        if getattr(self.objectified, 'Cnt', None) is not None:
            for meter in self.objectified.Cnt:
                meters.append(self.meter_class(meter, self.name))
            for meter in meters:
                self._warnings.append(meter.warnings)
        return meters


class BaseElement(object):
    """
    Base class
    """

    def __init__(self, objectified):
        """
        Create object.

        :param objectified: an lxml.objectify.StringElement
        :return: object
        """
        self.objectified = objectified
        self._warnings = []

    @property
    def objectified(self):
        """
        A lxml.objectify.StringElement.

        :return: an lxml.objectify.StringElement
        """
        return self._objectified

    @objectified.setter
    def objectified(self, value):
        """
        Stores an lxml.objectify.StringElement.

        :param value: an lxml.objectify.StringElement
        """
        self._objectified = value

    @property
    def name(self):
        """
        The name

        :return: a string with the name
        """
        return self.objectified.get('Id')

    @property
    def warnings(self):
        """
        Warnings

        :return: a list with the errors found while reading
        """
        return self._warnings
    

class LineSupervisor(BaseElement):
    """
    Base class for a line supervisor.
    """

    @property
    def errors(self):
        """
        The line supervisor errors.

        :return: a dict with the line supervisor errors
        """
        self._errors = {}
        if self.objectified.get('ErrCat'):
            self._errors = {
                'errcat': self.objectified.get('ErrCat'),
                'errcode': self.objectified.get('ErrCode')
            }
        return self._errors

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
        Measure set objects of this line supervisor.

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
        Values of measure sets of this line supervisor.

        :return: a list with the values of the measure sets
        """
        values = []
        for measure in self.measures:
            values.append(measure.value())
        return values


class LineSupervisorDetails(LineSupervisor):
    """
    Base class for a line supervisors of report that need the name of the remote terminal unit in the values, like S52.
    """
    def __init__(self, objectified_line_supervisor, rt_unit_name):
        """
        Create a line supervisor object using line supervisor constructor and adding the remote terminal unit name.

        :param objectified_line_supervisor: an lxml.objectify.StringElement representing a line supervisor
        :param rt_unit_name: a string with the name of the remote terminal unit
        :return: a line supervisor object
        """
        super(LineSupervisorDetails, self).__init__(objectified_line_supervisor)
        self.rt_unit_name = rt_unit_name
        
    @property
    def report_type(self):
        return self.__class__.__name__[-3:]

    @property
    def rt_unit_name(self):
        """
        A string with the remote terminal unit name.

        :return: a string with the remote terminal unit name
        """
        return self._rt_unit_name

    @rt_unit_name.setter
    def rt_unit_name(self, value):
        """
        Stores a string with the remote terminal unit name.

        :param value: a string with the remote terminal unit name
        """
        self._rt_unit_name = value

    @property
    def values(self):
        """
        Values of measure sets of this line supervisor of report that need the name of the remote terminal unit and the line supervisor

        :return: a list with the values of the measure sets
        """
        values = []
        for measure in self.measures:
            for subvalue in measure.values:
                v = subvalue.copy()
                v['name'] = self.name
                v['rt_unit_name'] = self.rt_unit_name
                values.append(v)
            if measure.warnings:
                if self._warnings.get(self.name, False):
                    self._warnings[self.name].extend(measure.warnings)
                else:
                    self._warnings.update({self.name: measure.warnings})
        return values

    @property
    def magnitude(self):
        """
        The magnitude of the line supervisor measures.

        :return: a int with the magnitude of the line supervisor measures
        """
        return int(self.objectified.get('Magn'))

    @property
    def position(self):
        """
        The position of the line supervisor measures.

        :return: a int with the position of the line supervisor measures
        """
        return int(self.objectified.get('Pos'))


class RemoteTerminalUnitDetails(BaseElement):
    """
    Base class for a remote terminal unit of report that need the name in the values, like S52.
    """

    @property
    def line_supervisor_class(self):
        """
        The class to instance line supervisors.

        :return: a class to instance line supervisors
        """
        return LineSupervisor

    @property
    def values(self):
        """
        Values of the line supervisors of this remote terminal unit.

        :return: a list with the values of the line supervisors
        """
        values = []
        for line_supervisor in self.line_supervisors:
            values.extend(line_supervisor.values)
        return values

    @property
    def line_supervisors(self):
        """
        Line supervisor objects of this remote terminal unit. The name of remote terminal unit is passed to the line supervisor.

        :return: a list of line supervisor objects
        """
        line_supervisors = []
        if getattr(self.objectified, 'LVSLine', None) is not None:
            for line_supervisor in self.objectified.LVSLine:
                line_supervisors.append(self.line_supervisor_class(line_supervisor, self.name))
            for line_supervisor in line_supervisors:
                self._warnings.append(line_supervisor.warnings)
        return line_supervisors
