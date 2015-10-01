from primestg.message import MessageS
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


class MeasureS02(MeasureActiveReactive):
    """
    Class for a set of measures of report S02.
    """

    @property
    def values(self):
        """
        Set of measures of report S02.

        :return: a dict with a set of measures of report S02
        """
        values = self.active_reactive(self.objectified, '')
        values.update(
            {
                'timestamp': self._get_timestamp('Fh'),
                'season': self.objectified.get('Fh')[-1:],
                'bc': self.objectified.get('Bc')
            }
        )
        return values


class MeasureS04(MeasureActiveReactive):
    """
    Class for a set of measures of report S04.
    """

    @property
    def values(self):
        """
        Set of measures of report S04.

        :return: a dict with a set of measures of report S04
        """
        values = []
        common_values = {
            'type': 'month',
            'date_begin': self._get_timestamp('Fhi'),
            'date_end': self._get_timestamp('Fhf'),
            'contract': int(self.objectified.get('Ctr')),
            'period': int(self.objectified.get('Pt')),
            'max': int(self.objectified.get('Mx')),
            'date_max': self._get_timestamp('Fx')
        }
        for s04_values in self.objectified.Value:
            v = common_values.copy()
            if s04_values.get('AIa'):
                measure_type = 'a'
            else:
                measure_type = 'i'
            v.update(self.active_reactive(s04_values, measure_type))
            v['value'] = measure_type
            values.append(v)
        return values


class MeasureS05(MeasureActiveReactive):
    """
    Class for a set of measures of report S05.
    """

    @property
    def values(self):
        """
        Set of measures of report S05.

        :return: a dict with a set of measures of report S05
        """
        values = []
        timestamp = self._get_timestamp('Fh')
        v = {
            'type': 'day',
            'value': 'a',
            'date_begin': timestamp,
            'date_end': timestamp,
            'contract': int(self.objectified.get('Ctr')),
            'period': int(self.objectified.get('Pt')),
        }

        for s05_values in self.objectified.Value:
            v.update(self.active_reactive(s05_values, 'a'))
            values.append(v)

        return values


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


class ParameterS06(Parameter):
    """
    Class for a set of parameters of report S06.
    """

    def __init__(
            self,
            objectified_parameter,
            report_version,
            concentrator_name,
            request_id,
            meter_name
    ):
        """
        Create a ParameterS06 object.

        :param objectified_parameter: an lxml.objectify.StringElement \
            representing a set of parameters
        :return: a Measure object
        """
        super(ParameterS06, self).__init__(
            objectified_parameter,
            report_version
        )
        self.concentrator_name = concentrator_name
        self.request_id = request_id
        self.meter_name = meter_name

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
    def request_id(self):
        """
        The request identification.

        :return: a string with the request identification
        """
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        """
        Stores the request identification.

        :param value: a string with the version of the report
        """
        self._request_id = value

    @property
    def meter_name(self):
        """
        The meter name.

        :return: a string with the meter name
        """
        return self._meter_name

    @meter_name.setter
    def meter_name(self, value):
        """
        Stores the meter name.

        :param value: a string with the meter name
        """
        self._meter_name = value

    @property
    def values(self):
        """
        Set of parameters of report S06.

        :return: a dict with a set of parameters of report S06
        """
        get = self.objectified.get

        values = {
            'request_id': self.request_id,
            'version': self.report_version,
            'concentrator': self.concentrator_name,
            'meter': self.meter_name,
            'timestamp': self._get_timestamp('Fh'),
            'season': get('Fh')[-1:],
            'serial_number': get('NS'),
            'manufacturer': get('Fab'),
            'model_type': get('Mod'),
            'manufacturing_year': int(get('Af')),
            'equipment_type': get('Te'),
            'firmware_version': get('Vf'),
            'prime_firmware_version': get('VPrime'),
            'protocol': get('Pro'),
            'id_multicast': get('Idm'),
            'mac': get('Mac'),
            'primary_voltage': int(get('Tp')),
            'secondary_voltage': int(get('Ts')),
            'primary_current': int(get('Ip')),
            'secondary_current': int(get('Is')),
            'time_threshold_voltage_sags': int(get('Usag')),
            'time_threshold_voltage_swells': int(get('Uswell')),
            'load_profile_period': int(get('Per')),
            'demand_close_contracted_power': get('Dctcp'),
            'reference_voltage': int(get('Vr')),
            'long_power_failure_threshold': int(get('Ut')),
            'voltage_sag_threshold': get('UsubT'),
            'voltage_swell_threshold': get('UsobT'),
            'voltage_cut-off_threshold': get('UcorteT'),
            'automatic_monthly_billing': self.get_boolean('AutMothBill'),
            'scroll_display_mode': get('ScrollDispMode'),
            'time_scroll_display': int(get('ScrollDispTime'))
        }
        return values


class ParameterS12(Parameter):
    """
    Class for a set of parameters of report S12.
    """

    @property
    def values(self):
        """
        Set of parameters of report S12.

        :return: a dict with a set of parameters of report S12
        """
        get = self.objectified.get

        if self.report_version == '3.1c':
            fwmtup_timeout_key = 'TimeOutMeterFwU'
        else:
            fwmtup_timeout_key = 'TimeOutPrimeFwU'

        fwmtup_timeout = self.to_integer(get(fwmtup_timeout_key))

        # Ormazabal Current concentrators returns the IPftp1 field
        if 'IPftp' in self.objectified.keys():
            rpt_ftp_ip_address_key = 'IPftp'
        else:
            rpt_ftp_ip_address_key = 'IPftp1'

        rpt_ftp_ip_address = get(rpt_ftp_ip_address_key)

        ntp_max_deviation = self.filter_integer(get('NTPMaxDeviation'))
        session_timeout = self.filter_integer(get('AccInacTimeout'))
        max_sessions = self.filter_integer(get('AccSimulMax'))

        values = {
            'date': self._get_timestamp('Fh'),
            'model': get('Mod'),
            'mf_year': get('Af'),
            'type': get('Te'),
            'w_password': get('DCPwdAdm'),
            'r_password': get('DCPwdRead'),
            'fw_version': get('Vf'),
            'fw_comm_version': get('VfComm'),
            'protocol': get('Pro'),
            'communication': get('Com'),
            'battery_mon': get('Bat'),
            'ip_address': get('ipCom'),
            'dc_ws_port': get('PortWS'),
            'ip_mask': get('ipMask'),
            'ip_gtw': get('ipGtw'),
            'dhcp': self.get_boolean('ipDhcp'),
            'slave1': get('Slave1'),
            'slave2': get('Slave2'),
            'slave3': get('Slave3'),
            'local_ip_address': get('ipLoc'),
            'local_ip_mask': get('ipMaskLoc'),
            'plc_mac': get('Macplc'),
            'serial_port_speed': get('Pse'),
            'priority': self.get_boolean('Priority'),
            'stg_ws_ip_address': get('IPstg'),
            'stg_ws_password': get('stgPwd'),
            'ntp_ip_address': get('IPNTP'),
            'rpt_ftp_ip_address': rpt_ftp_ip_address,
            'rpt_ftp_user': get('FTPUserReport'),
            'rpt_ftp_password': get('FTPPwdReport'),
            'fwdcup_ftp_ip_address': get('IPftpDCUpg'),
            'fwdcup_ftp_user': get('UserftpDCUpg'),
            'fwdcup_ftp_password': get('PwdftpDCUpg'),
            'fwmtup_ftp_ip_address': get('IPftpMeterUpg'),
            'fwmtup_ftp_user': get('UserftpMeterUpg'),
            'fwmtup_ftp_password': get('UserftpMeterUpg'),
            'retries': int(get('RetryFtp')),
            'time_btw_retries': int(get('TimeBetwFtp')),
            'cycle_ftp_ip_address': get('IPftpCycles'),
            'cycle_ftp_user': get('UserftpCycles'),
            'cycle_ftp_password': get('PwdftpCycles'),
            'cycle_ftp_dir': get('DestDirCycles'),
            'sync_meter': self.get_boolean('SyncMeter'),
            'fwmtup_timeout': fwmtup_timeout,
            'max_time_deviation': int(get('TimeDevOver')),
            'min_time_deviation': int(get('TimeDev')),
            'reset_msg': self.get_boolean('ResetMsg'),
            'rpt_meter_limit': int(get('NumMeters')),
            'rpt_time_limit': int(get('TimeSendReq')),
            'disconn_time': int(get('TimeDisconMeter')),
            'disconn_retries': int(get('RetryDisconMeter')),
            'disconn_retry_interval': int(get('TimeRetryInterval')),
            'meter_reg_data': get('MeterRegData'),
            'report_format': get('ReportFormat'),
            's26_content': get('S26Content'),
            'values_check_delay': int(get('ValuesCheckDelay')),
            'max_order_outdate': self.to_integer(get('MaxOrderOutdate')),
            'restart_delay': self.to_integer(get('TimeDelayRestart')),
            'ntp_max_deviation': ntp_max_deviation,
            'session_timeout': session_timeout,
            'max_sessions':  max_sessions
        }
        if hasattr(self.objectified, 'TP'):
            tasks = []
            for task in self.objectified.TP:
                task_values = {
                    'name': task.get('TpTar'),
                    'priority': int(task.get('TpPrio')),
                    'date_from': self._get_timestamp('TpHi', element=task),
                    'periodicity': task.get('TpPer'),
                    'complete': self.get_boolean('TpCompl', element=task),
                    'meters': task.get('TpMet'),
                }
                task_data_values = []
                for task_data in task.TpPro:
                    task_data_value = {
                        'request': task_data.get('TpReq'),
                        'stg_send':
                            self.get_boolean('TpSend', element=task_data),
                        'store':
                            self.get_boolean('TpStore', element=task_data),
                        'attributes': task_data.get('TpAttr'),
                    }
                    task_data_values.append(task_data_value)
                task_values['task_data'] = task_data_values
                tasks.append(task_values)
            values['tasks'] = tasks
        else:
            values['tasks'] = []
        return values


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
        return self.objectified.get('Magn')

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
            meter and the magnitude.

        :return: a list with the values of the measure sets
        """
        values = []
        for measure in self.measures:
            v = measure.values.copy()
            v['name'] = self.name
            v['magn'] = int(self.magnitude)
            values.append(v)
        if values:
            return values
        else:
            return {}


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


class MeterS04(MeterWithConcentratorName):
    """
    Class for a meter of report S04.
    """

    @property
    def report_type(self):
        """
        The type of report for report S04.

        :return: a string with 'S04'
        """
        return 'S04'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S04.

        :return: a class to instance measure sets of report S04
        """
        return MeasureS04


class MeterS05(MeterWithConcentratorName):
    """
    Class for a meter of report S05.
    """

    @property
    def report_type(self):
        """
        The type of report for report S05.

        :return: a string with 'S05'
        """

        return 'S05'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S05.

        :return: a class to instance measure sets of report S05
        """
        return MeasureS05


class MeterS06(MeterWithConcentratorName):
    """
    Class for a meter of report S06.
    """

    def __init__(
            self,
            objectified_meter,
            concentrator_name,
            report_version,
            request_id
    ):
        """
        Create a Meter object using MeterWithConcentratorName constructor and \
            adding the report version and request identification.

        Create a Meter object.

        :param objectified_meter: an lxml.objectify.StringElement \
            representing a set of parameters
        :param concentrator_name: a string with the name of the concentrator
        :param report_version: a string with the version of report
        :param request_id: a string with the request identification
        :return: a Measure object
        """
        super(MeterS06, self).__init__(objectified_meter, concentrator_name)
        self.report_version = report_version
        self.request_id = request_id

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

    @property
    def request_id(self):
        """
        The request identification.

        :return: a string with the request identification
        """
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        """
        Stores the request identification.

        :param value: a string with the version of the report
        """
        self._request_id = value

    @property
    def parameters(self):
        """
        Parameter set objects of this concentrator.

        :return: a list of parameter set objects
        """
        parameters = []
        for parameter in self.objectified.S06:
            parameters.append(ParameterS06(
                parameter,
                self.report_version,
                self.concentrator_name,
                self.request_id,
                self.name
            ))
        return parameters

    @property
    def values(self):
        """
        Values of the set of parameters of this meter.

        :return: a list with the values of the meter
        """
        values = []
        for parameter in self.parameters:
            values.append(parameter.values)
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


class ConcentratorS04(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S04.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S04.

        :return: a class to instance meters of report S04
        """
        return MeterS04


class ConcentratorS05(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S05.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S05.

        :return: a class to instance meters of report S05
        """
        return MeterS05


class ConcentratorS06(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S06.
    """

    def __init__(self, objectified_concentrator, report_version, request_id):
        """
        Create a Concentrator object for the report S06 using \
            ConcentratorWithMetersWithConcentratorName constructor and adding \
            the report version and request identification.

        :param objectified_concentrator: an lxml.objectify.StringElement \
            representing a meter
        :param report_version: a string with the version of report
        :param request_id: a string with the request identification
        :return: a Meter object
        """
        super(ConcentratorS06, self).__init__(objectified_concentrator)
        self.report_version = report_version
        self.request_id = request_id

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

    @property
    def request_id(self):
        """
        The request identification.

        :return: a string with the request identification
        """
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        """
        Stores the request identification.

        :param value: a string with the version of the report
        """
        self._request_id = value

    @property
    def meters(self):
        """
        Meter objects of this concentrator.

        :return: a list of meter objects
        """
        meters = []
        for meter in self.objectified.Cnt:
            meters.append(MeterS06(
                meter,
                self.name,
                self.report_version,
                self.request_id
            ))
        return meters


class ConcentratorS12(Concentrator):
    """
    Class for a concentrator of report S12.
    """

    def __init__(self, objectified_concentrator, report_version):
        """
        Create a Concentrator object for the report S12.

        :param objectified_concentrator: an lxml.objectify.StringElement \
            representing a meter
        :param report_version: a string with the version of report
        :return: a Meter object
        """
        super(ConcentratorS12, self).__init__(objectified_concentrator)
        self.report_version = report_version

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

    @property
    def parameters(self):
        """
        Parameter set objects of this concentrator.

        :return: a list of parameter set objects
        """
        parameters = []
        for parameter in self.objectified.S12:
            parameters.append(ParameterS12(parameter, self.report_version))
        return parameters

    @property
    def values(self):
        """
        Values of the set of parameters of this concentrator.

        :return: a list with the values of the meters
        """
        values = []
        for parameter in self.parameters:
            values.append(parameter.values)
        return values


class Report(object):
    """
    Report class to process MessageS
    """

    def __init__(self, report):
        """
        Creates a Report object.

        :param report: a file object or a string with the XML or a MessageS \
            object
        :return: an Report object
        """
        self.message = report

    @property
    def message(self):
        """
        A message as a MessageS object.

        :return: a MessageS object
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        Stores the message as a MessageS.

        :param value: a file object or a string with the XML or a MessageS \
            object
        """
        if isinstance(value, (file, basestring)):
            message = MessageS(value)
        elif isinstance(value, MessageS):
            message = value
        else:
            error = 'must be file or basestring with XML or a MessageS'
            raise TypeError(error)

        self._message = message

    @property
    def report_type(self):
        """
        The report type.

        :return: a string with the report type
        """
        return self.message.objectified.get('IdRpt')

    @property
    def report_version(self):
        """
        The report version.

        :return: a string with the report version
        """
        return self.message.objectified.get('Version')

    @property
    def request_id(self):
        """
        The report version.

        :return: a string with the report version
        """
        return self.message.objectified.get('IdPet')

    def get_concentrator(self, objectified_concentrator):
        """
        Instances a concentrator object

        :return: a concentrator object
        """
        report_type_class = {
            'S02': {
                'class': ConcentratorS02,
                'args': [objectified_concentrator]
            },
            'S04': {
                'class': ConcentratorS04,
                'args': [objectified_concentrator]
            },
            'S05': {
                'class': ConcentratorS05,
                'args': [objectified_concentrator]
            },
            'S06': {
                'class': ConcentratorS06,
                'args': [
                    objectified_concentrator,
                    self.report_version,
                    self.request_id
                ]
            },
            'S12': {
                'class': ConcentratorS12,
                'args': [objectified_concentrator, self.report_version]
            }
        }

        if self.report_type not in report_type_class:
            raise NotImplementedError('Report type not implemented!')

        get = report_type_class.get(self.report_type).get
        concentrator_class = get('class')
        concentrator_args = get('args')
        concentrator = concentrator_class(*concentrator_args)
        return concentrator

    @property
    def concentrators(self):
        """
        The concentrators of the report.

        :return: a list of concentrators of the report
        """
        return map(self.get_concentrator, self.message.objectified.Cnc)

    @property
    def values(self):
        """
        Values of the whole report.

        :return: a list with the values of the whole report
        """
        values = []
        for concentrator in self.concentrators:
            values.extend(concentrator.values)
        return values
