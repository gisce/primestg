from primestg.report.base import (
    MeasureActiveReactive, MeasureActiveReactiveFloat, Parameter,
    MeterWithMagnitude, ConcentratorWithMetersWithConcentratorName,
    Concentrator, Measure, MeterWithConcentratorName, LineSupervisorDetails, RemoteTerminalUnitDetails,
    Operation, MeasureAverageVoltageAndCurrent
)
from primestg.message import MessageS
from primestg.utils import octet2name, octet2number

SUPPORTED_REPORTS = ['S02', 'S04', 'S05', 'S06', 'S09', 'S12', 'S13', 'S14', 'S15',
                     'S17', 'S18', 'S23', 'S24', 'S27', 'S42', 'S52']


def is_supported(report_code):
    return report_code in SUPPORTED_REPORTS


def get_integer_value(param):
    try:
        result = int(param)
    except ValueError as e:
        result = 0
    return result


def get_float_value(param):
    try:
        result = float(param)
    except ValueError as e:
        result = 0.0
    return result


class MeasureS01(MeasureActiveReactive):
    """
    Class for a set of measures of report S01.
    """
    @property
    def values(self):
        """
        Set of measures of report S01.
        :return: a dict with a set of measures of report S01.
        """
        values = {}
        try:
            get = self.objectified.get
            values = self.active_reactive(self.objectified, 'a')
            values.update(
                {
                    'timestamp': self._get_timestamp('Fh'),
                    'voltage': get_integer_value(get('L1v')),
                    'current': get_float_value(get('L1i')),
                    'active_power_import': get_integer_value(get('Pimp')),
                    'active_power_export': get_integer_value(get('Pexp')),
                    'reactive_power_import': get_integer_value(get('Qimp')),
                    'reactive_power_export': get_integer_value(get('Qexp')),
                    'power_factor': get_float_value(get('PF')),
                    'active_quadrant': get_integer_value(get('Ca')),
                    'phase_presence': [get_integer_value(i) for i in (get('PP')).split(",")],
                    'meter_phase': get_integer_value(get('Fc')),
                    'current_switch_state': get_integer_value(get('Eacti')),
                    'previous_switch_state': get_integer_value(get('Eanti')),
                }
            )
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
            return []
        return [values]


class MeasureS21(MeasureActiveReactive):
    """
    Class for a set of measures of report S21.
    """
    @property
    def values(self):
        """
        Set of measures of report S21.
        :return: a dict with a set of measures of report S21.
        """
        values = {}
        try:
            get = self.objectified.get
            values = self.active_reactive(self.objectified, 'a')
            values.update(
                {
                    'timestamp': self._get_timestamp('Fh'),
                    'active_quadrant': get_integer_value(get('Ca')),
                    'current_sum_3_phases': get_float_value(get('I3')),

                    'voltage1': get_integer_value(get('L1v')),
                    'current1': get_float_value(get('L1i')),
                    'active_power_import1': get_integer_value(get('Pimp1')),
                    'active_power_export1': get_integer_value(get('Pexp1')),
                    'reactive_power_import1': get_integer_value(get('Qimp1')),
                    'reactive_power_export1': get_integer_value(get('Qexp1')),
                    'power_factor1': get_float_value(get('PF1')),
                    'active_quadrant_phase1': get_integer_value(get('Ca1')),

                    'voltage2': get_integer_value(get('L2v')),
                    'current2': get_float_value(get('L2i')),
                    'active_power_import2': get_integer_value(get('Pimp2')),
                    'active_power_export2': get_integer_value(get('Pexp2')),
                    'reactive_power_import2': get_integer_value(get('Qimp2')),
                    'reactive_power_export2': get_integer_value(get('Qexp2')),
                    'power_factor2': get_float_value(get('PF2')),
                    'active_quadrant_phase2': get_integer_value(get('Ca2')),

                    'voltage3': get_integer_value(get('L3v')),
                    'current3': get_float_value(get('L3i')),
                    'active_power_import3': get_integer_value(get('Pimp3')),
                    'active_power_export3': get_integer_value(get('Pexp3')),
                    'reactive_power_import3': get_integer_value(get('Qimp3')),
                    'reactive_power_export3': get_integer_value(get('Qexp3')),
                    'power_factor3': get_float_value(get('PF3')),
                    'active_quadrant_phase3': get_integer_value(get('Ca3')),

                    'phase_presence': [get_integer_value(i) for i in (get('PP')).split(",")],
                    'meter_phase': get_integer_value(get('Fc')),
                    'current_switch_state': get_integer_value(get('Eacti')),
                    'previous_switch_state': get_integer_value(get('Eanti')),
                }
            )
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
            return []
        return [values]


class MeasureS02(MeasureActiveReactiveFloat):
    """
    Class for a set of measures of report S02.
    """

    @property
    def values(self):
        """
        Set of measures of report S02.

        :return: a dict with a set of measures of report S02
        """
        values = {}
        try:
            values = self.active_reactive(self.objectified, '')
            values.update(
                {
                    'timestamp': self._get_timestamp('Fh'),
                    'season': self.objectified.get('Fh')[-1:],
                    'bc': self.objectified.get('Bc')
                }
            )
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
            return []

        return [values]


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
        try:
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
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
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
        try:
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
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))

        return values


class MeasureS14(MeasureAverageVoltageAndCurrent):
    """
    Class for a set of measures of report S14.
    """

    @property
    def values(self):
        """
        Set of measures of report S14.

        :return: a dict with a set of measures of report S14
        """
        try:
            values = self.average_voltage_and_current(self.objectified)
            values.update(
                {
                    'timestamp': self._get_timestamp('Fh'),
                    'season': self.objectified.get('Fh')[-1:],
                    'bc': self.objectified.get('Bc'),
                    'simp': int(self.objectified.get('Simp')),
                    'sexp': int(self.objectified.get('Sexp'))
                }
            )
            return [values]

        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))


class MeasureS27(MeasureActiveReactive):
    """
    Class for a set of measures of report S27.
    """

    @property
    def values(self):
        """
        Set of measures of report S27.

        :return: a dict with a set of measures of report S27
        """
        values = []
        try:
            timestamp = self._get_timestamp('Fh')
            timestamp_max = self._get_timestamp('Fx')
            v = {
                'type': 'manual',
                'value': 'a',
                'date_begin': timestamp,
                'date_end': timestamp,
                'contract': int(self.objectified.get('Ctr')),
                'period': int(self.objectified.get('Pt')),
                'max': int(self.objectified.get('Mx')),
                'date_max': timestamp_max
            }

            for s27_values in self.objectified.Value:
                v.update(self.active_reactive(s27_values, 'a'))
                values.append(v)
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))

        return values


class OperationS42(Operation):
    """
    Class for a set of measures of report S42.
    """

    @property
    def values(self):
        """
        Set of measures of report S42.
        :return: a dict with a set of measures of report S42
        """
        values = []
        try:
            common_values = {
                "Fh": self._get_timestamp('Fh'),
                "Operation": self.objectified.get('Operation'),
                "obis": self.objectified.get('obis'),
                "class": self.objectified.get('class'),
                "element": self.objectified.get('element'),
                "data": self.objectified.get('data'),
                "result": self.objectified.get('result'),
            }
            values.append(common_values)
        except Exception as e:
            values.append(['ERROR: Thrown exception: {}'.format(e)])
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
        return values


class MeasureS52(MeasureActiveReactiveFloat):
    """
    Class for a set of measures of report S52.
    """

    @property
    def values(self):
        """
        Set of measures of report S52.

        :return: a dict with a set of measures of report S52
        """
        try:
            values = self.active_reactive(self.objectified, '')
            values.update(
                {
                    'timestamp': self._get_timestamp('Fh'),
                    'bc': self.objectified.get('Bc')
                }
            )
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
            return []

        return [values]


class MeasureEvents(Measure):
    """
    Class for a set of measures of report S09.
    """

    @property
    def values(self):
        """
        Set of measures of report S09.

        :return: a dict with a set of measures of report S09
        """
        values = []
        try:
            timestamp = self._get_timestamp('Fh')
            v = {
                'timestamp': timestamp,
                'event_group': int(self.objectified.get('Et')),
                'season': self.objectified.get('Fh')[-1:],
                'event_code': int(self.objectified.get('C')),
            }
            data = ''
            d1s = ['D1: {}'.format(d)
                   for d in getattr(self.objectified, 'D1', [])]
            d2s = ['D2: {}'.format(d)
                   for d in getattr(self.objectified, 'D2', [])]
            data = '\n'.join(d1s + d2s)
            if data:
                v.update({'data': data})

            values.append(v)
        except Exception as e:
            self._warnings.append('ERROR: Reading a meter event. Thrown '
                                  'exception: {}'.format(e))

        return values


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
        values = {}
        try:
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
                'manufacturing_year': get_integer_value(get('Af')),
                'equipment_type': get('Te'),
                'firmware_version': get('Vf'),
                'prime_firmware_version': get('VPrime'),
                'protocol': get('Pro'),
                'id_multicast': get('Idm'),
                'mac': get('Mac'),
                'primary_voltage': get_integer_value(get('Tp')),
                'secondary_voltage': get_integer_value(get('Ts')),
                'primary_current': get_integer_value(get('Ip')),
                'secondary_current': get_integer_value(get('Is')),
                'time_threshold_voltage_sags': get_integer_value(get('Usag')),
                'time_threshold_voltage_swells': get_integer_value(get('Uswell')),
                'load_profile_period': get_integer_value(get('Per')),
                'demand_close_contracted_power': get('Dctcp'),
                'reference_voltage': get_integer_value(get('Vr')),
                'long_power_failure_threshold': get_integer_value(get('Ut')),
                'voltage_sag_threshold': get('UsubT'),
                'voltage_swell_threshold': get('UsobT'),
                'voltage_cut-off_threshold': get('UcorteT'),
                'automatic_monthly_billing': self.get_boolean('AutMothBill'),
                'scroll_display_mode': get('ScrollDispMode'),
                'time_scroll_display': get_integer_value(get('ScrollDispTime'))
            }
        except Exception as e:
            self._warnings.append('ERROR: Cnc({}), Meter({}). Thrown '
                                  'exception: {}'.format(self.concentrator_name,
                                                         self.meter_name, e))
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
        values = {}

        try:
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
                    if getattr(task, 'TpPro', None) is not None:
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
        except Exception as e:
            self._warnings.append('ERROR: Reading S12 report. Thrown '
                                  'exception: {}'.format(e))
        return values


class ParameterS23(Parameter):
    """
    Class for a set of parameters of report S23.
    """

    """
    Static method to retrieve values with common structure for S23.

    :return: formated values for PCact and PCLatent sections 
    """
    @staticmethod
    def get_pc(obj):
        obj_values = {}
        if obj.get('ActDate'):
            obj_values.update({'act_date': Measure(obj)._get_timestamp('ActDate')})
        if getattr(obj, 'Contrato1', None) is not None:
            for obj_data in obj.Contrato1:
                obj_contrato1_value = {
                    'tr1': int(obj_data.get('TR1')),
                    'tr2': int(obj_data.get('TR2')),
                    'tr3': int(obj_data.get('TR3')),
                    'tr4': int(obj_data.get('TR4')),
                    'tr5': int(obj_data.get('TR5')),
                    'tr6': int(obj_data.get('TR6')),
                }
            obj_values.update({'contrato1': obj_contrato1_value})
        if getattr(obj, 'PResidual', None) is not None:
            for obj_data in obj.PResidual:
                obj_presidual_value = {
                    'tr1': int(obj_data.get('TR1')),
                    'tr2': int(obj_data.get('TR2')),
                    'tr3': int(obj_data.get('TR3')),
                    'tr4': int(obj_data.get('TR4')),
                    'tr5': int(obj_data.get('TR5')),
                    'tr6': int(obj_data.get('TR6')),
                }
            obj_values.update({'presidual': obj_presidual_value})
        return obj_values

    """
    Static method to retrieve values with common structure for S23.

    :return: formated values for ActiveCalendar and LatentCalendar sections
    """
    @staticmethod
    def get_calendars(obj, is_active_calendar=False):
        obj_values = {}
        if getattr(obj, 'Contract', None) is not None:
            contracts = []
            for i, contract_obj in enumerate(obj.Contract):
                contract = {
                    'c': contract_obj.get('c'),
                    'calendar_type': contract_obj.get('CalendarType'),
                    'calendar_name': octet2name(contract_obj.get('CalendarName')),
                    'act_date': Measure(contract_obj)._get_timestamp('ActDate'),
                    'is_active_calendar': is_active_calendar
                }
                if getattr(contract_obj, 'Season', None) is not None:
                    seasons = []
                    for x, season_obj in enumerate(contract_obj.Season):
                        season = {
                            'name': season_obj.get('Name'),
                            'start': season_obj.get('Start'),
                            'week': season_obj.get('Week'),
                        }
                        seasons.append(season)
                    contract.update({'seasons': seasons})
                if getattr(contract_obj, 'Week', None) is not None:
                    weeks = []
                    for x, week_obj in enumerate(contract_obj.Week):
                        week_days = week_obj.get('Week')
                        week = {
                            'name': week_obj.get('Name'),
                            'week': week_obj.get('Week'),
                            'index': x,
                        }
                        for index in range(0, len(week_days), 2):
                            day = 'day{}'.format(int(index/2))
                            week.update({day: week_days[index:index+2]})
                        weeks.append(week)
                    contract.update({'weeks': weeks})
                if getattr(contract_obj, 'SpecialDays', None) is not None:
                    special_days = []
                    for x, special_day_obj in enumerate(contract_obj.SpecialDays):
                        special_day = {
                            'dt': Measure(special_day_obj)._get_special_days('DT'),
                            'dt_card': False if special_day_obj.get('DTCard', 'N') == 'N' else True,
                            'day_id': special_day_obj.get('DayID'),
                        }
                        special_days.append(special_day)
                    contract.update({'special_days': special_days})
                if getattr(contract_obj, 'Day', None) is not None:
                    days = []
                    for x, day_obj in enumerate(contract_obj.Day):
                        day = {'day_id': day_obj.get('id', None)}
                        changes = []
                        if contract_obj.Day[x].getchildren():
                            for y, change_obj in enumerate(contract_obj.Day[x].Change):
                                if getattr(day_obj, 'Change', None) is not None:
                                    change = {
                                        'hour': octet2number(change_obj.get('Hour', '00')[0:2]),
                                        'tariffrate': change_obj.get('TariffRate'),
                                    }
                                    changes.append(change)
                            day.update({'changes': changes})
                        days.append(day)
                    contract.update({'days': days})
                contracts.append(contract)
            obj_values.update({'contracts': contracts})
        return obj_values

    @property
    def values(self):
        """
        Set of parameters of report S23.

        :return: a dict with a set of parameters of report S23
        """
        values = {}
        try:
            values.update({'date': self._get_timestamp('Fh')})
            if hasattr(self.objectified, 'PCact'):
                pc_act = self.objectified.PCact
                obj_values = self.get_pc(pc_act)
                values['pc_act'] = obj_values
            else:
                values['pc_act'] = 'supervisor'
            if hasattr(self.objectified, 'PCLatent'):
                pc_lat = self.objectified.PCLatent
                obj_values = self.get_pc(pc_lat)
                values['pc_latent'] = obj_values
            else:
                values['pc_act'] = 'supervisor'
            if hasattr(self.objectified, 'ActiveCalendars'):
                active_calendars = self.objectified.ActiveCalendars
                obj_values = self.get_calendars(active_calendars, True)
                values['active_calendars'] = obj_values
            else:
                values['active_calendars'] = []
            if hasattr(self.objectified, 'LatentCalendars'):
                latent_calendars = self.objectified.LatentCalendars
                obj_values = self.get_calendars(latent_calendars, False)
                values['latent_calendars'] = obj_values
            else:
                values['latent_calendars'] = []
        except Exception as e:
            self._warnings.append('ERROR: Reading S23 report. Thrown '
                                  'exception: {}'.format(e))
        return values


class ParameterS24(Parameter):
    """
    Class for a set of parameters of report S24.
    """

    def __init__(
            self,
            objectified_parameter,
            report_version,
            concentrator_name,
            request_id
    ):
        """
        Create a ParameterS24 object.

        :param objectified_parameter: an lxml.objectify.StringElement \
            representing a set of parameters
        :return: a Measure object
        """
        super(ParameterS24, self).__init__(
            objectified_parameter,
            report_version
        )
        self.concentrator_name = concentrator_name
        self.request_id = request_id

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
    def values(self):
        """
        Set of parameters of report S24.

        :return: a dict with a set of parameters of report S24
        """
        values = {}

        try:
            timestamp = self._get_timestamp('Fh')
            values = {
                'timestamp': timestamp,
                'season': self.objectified.get('Fh')[-1:],
                'cnc_name': self.concentrator_name,
                'meters': []
            }
            for s24_meters in self.objectified.Meter:
                values['meters'].append(self.meter_availability(s24_meters))
        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
        return values


class ParameterConcentratorEvents(Parameter):
    """
    Class for a set of parameters of report S17.
    """

    def __init__(
            self,
            objectified_parameter,
            report_version,
            concentrator_name,
            request_id
    ):
        """
        Create a ParameterS17 object.

        :param objectified_parameter: an lxml.objectify.StringElement \
            representing a set of parameters
        :return: a Measure object
        """
        super(ParameterConcentratorEvents, self).__init__(
            objectified_parameter,
            report_version
        )
        self.concentrator_name = concentrator_name
        self.request_id = request_id

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
    def values(self):
        """
        Set of parameters of report S17.

        :return: a dict with a set of parameters of report S17
        """
        values = []
        try:
            get = self.objectified.get
            values = {
                'name': self.concentrator_name,
                'event_code': int(get('C')),
                'season': get('Fh')[-1:],
                'timestamp': self._get_timestamp('Fh'),
                'event_group': int(get('Et'))
            }

            data = ''
            d1s = ['D1: {}'.format(d)
                   for d in getattr(self.objectified, 'D1', [])]
            d2s = ['D2: {}'.format(d)
                   for d in getattr(self.objectified, 'D2', [])]
            data = '\n'.join(d1s + d2s)
            if data:
                values.update({'data': data})
        except Exception as e:
            self._warnings.append('ERROR: Reading a concentrator event. Thrown '
                                  'exception: {}'.format(e))
            return []

        return values


class LineSupervisorS52(LineSupervisorDetails):
    """
    Class for a line supervisor of report S52.
    """

    @property
    def report_type(self):
        """
        The type of report for report S52.

        :return: a string with 'S52'
        """
        return 'S52'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S52.

        :return: a class to instance measure sets of report S52
        """
        return MeasureS52

    @property
    def values(self):
        """
        Values of measure sets of this line supervisor of report that need the name of the remote terminal unit
        and the line supervisor

        :return: a list with the values of the measure sets
        """
        values = super(LineSupervisorS52, self).values
        for value in values:
            value['magn'] = self.magnitude
        return values


class MeterS01(MeterWithMagnitude):
    """
    Class for a meter of report S01.
    """

    @property
    def report_type(self):
        """
        The type of report for report S01.

        :return: a string with 'S01'
        """
        return 'S01'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S01.

        :return: a class to instance measure sets of report S01
        """
        return MeasureS01


class MeterS02(MeterWithMagnitude):
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
        Values of measure sets of this meter of report that need the name of \
            the concentrator and the meter,

        :return: a list with the values of the measure sets
        """
        values = super(MeterS02, self).values
        for value in values:
            value['magn'] = self.magnitude
        return values


class MeterS04(MeterWithMagnitude):
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


class MeterS05(MeterWithMagnitude):
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


class MeterS14(MeterWithConcentratorName):
    """
    Class for a meter of report S14.
    """

    @property
    def report_type(self):
        """
        The type of report for report S14.

        :return: a string with 'S14'
        """

        return 'S14'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S14.

        :return: a class to instance measure sets of report S14
        """
        return MeasureS14



class MeterS27(MeterWithMagnitude):
    """
    Class for a meter of report S27.
    """

    @property
    def report_type(self):
        """
        The type of report for report S27.

        :return: a string with 'S27'
        """

        return 'S27'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S27.

        :return: a class to instance measure sets of report S27
        """
        return MeasureS27


class MeterS06(MeterWithMagnitude):
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
            if parameter.warnings:
                if self._warnings.get(self.name, False):
                    self._warnings[self.name].extend(parameter.warnings)
                else:
                    self._warnings.update({self.name: parameter.warnings})
        return values

    @property
    def warnings(self):
        """
        Warnings of this meter.

        :return: a list with the errors found reading the meter
        """
        return self._warnings


class MeterS09(MeterWithConcentratorName):
    """
    Class for a meter of report S09.
    """

    @property
    def report_type(self):
        """
        The type of report for report S09.

        :return: a string with 'S09'
        """

        return 'S09'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S09.

        :return: a class to instance measure sets of report S09
        """
        return MeasureEvents


class MeterS13(MeterWithConcentratorName):
    """
    Class for a meter of report S09.
    """

    @property
    def report_type(self):
        """
        The type of report for report S09.

        :return: a string with 'S09'
        """

        return 'S13'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S09.

        :return: a class to instance measure sets of report S09
        """
        return MeasureEvents


class MeterS21(MeterWithMagnitude):
    """
    Class for a meter of report S21.
    """

    @property
    def report_type(self):
        """
        The type of report for report S21.

        :return: a string with 'S21'
        """
        return 'S21'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S21.

        :return: a class to instance measure sets of report S21
        """
        return MeasureS21


class MeterS23(MeterWithConcentratorName):
    """
    Class for a meter of report S23.
    """

    @property
    def report_type(self):
        """
        The type of report for report S23.

        :return: a string with 'S23'
        """

        return 'S23'

    """
    Class for a meter of report S23.
    """

    def __init__(
            self,
            objectified_meter,
            concentrator_name
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
        super(MeterS23, self).__init__(objectified_meter, concentrator_name)

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
        if not self.errors:
            parameters = []
            for parameter in self.objectified.S23:
                parameters.append(ParameterS23(
                    parameter,
                    self.concentrator_name,
                ))
        else:
            parameters = []
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
            if parameter.warnings:
                if self._warnings.get(self.name, False):
                    self._warnings[self.name].extend(parameter.warnings)
                else:
                    self._warnings.update({self.name: parameter.warnings})
        return values

    @property
    def warnings(self):
        """
        Warnings of this meter.

        :return: a list with the errors found reading the meter
        """
        return self._warnings

    @property
    def meters(self):
        """
        Meter objects of this concentrator.

        :return: a list of meter objects
        """
        meters = []
        if getattr(self.objectified, 'Cnt', None) is not None:
            for meter in self.objectified.Cnt:
                meters.append(MeterS23(
                    meter,
                    self.name,
                    self.report_version,
                    self.request_id
                ))
            for meter in meters:
                self._warnings.append(meter.warnings)
        return meters


class MeterS42(MeterWithConcentratorName):
    """
    Class for a meter of report S42.
    """

    @property
    def report_type(self):
        """
        The type of report for report S42.

        :return: a string with 'S42'
        """
        return 'S42'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S42.
        :return: a class to instance measure sets of report S42
        """
        return OperationS42


class ConcentratorS01(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S01.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S01.

        :return: a class to instance meters of report S01
        """
        return MeterS01


class ConcentratorS02(ConcentratorWithMetersWithConcentratorName):
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


class ConcentratorS27(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S27.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S27.

        :return: a class to instance meters of report S27
        """
        return MeterS27


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
        if getattr(self.objectified, 'Cnt', None) is not None:
            for meter in self.objectified.Cnt:
                meters.append(MeterS06(
                    meter,
                    self.name,
                    self.report_version,
                    self.request_id
                ))
            for meter in meters:
                self._warnings.append(meter.warnings)
        return meters


class ConcentratorS09(ConcentratorWithMetersWithConcentratorName):
    """
        Class for a concentrator of report S09.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S09.

        :return: a class to instance meters of report S09
        """
        return MeterS09


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
        if getattr(self.objectified, 'S12', None) is not None:
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
            self._warnings.extend(parameter.warnings)
        return values


class ConcentratorS13(ConcentratorWithMetersWithConcentratorName):
    """
        Class for a concentrator of report S13.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S09.

        :return: a class to instance meters of report S09
        """
        return MeterS13


class ConcentratorS14(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S14.
    """
    @property
    def meter_class(self):
        """
        The class used to instance meters for report S14.

        :return: a class to instance meters of report S14
        """
        return MeterS14



class ConcentratorEvents(Concentrator):
    """
    Class for a concentrator of report S17.
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
        super(ConcentratorEvents, self).__init__(objectified_concentrator)
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
    def values(self):
        """
        Values of the set of parameters of this concentrator.

        :return: a list with the values of the meters
        """
        values = []
        for parameter in self.parameters:
            if parameter.values:
                values.append(parameter.values)
            if parameter.warnings:
                self._warnings.extend(parameter.warnings)
        return values


class ConcentratorS15(ConcentratorEvents):

    def __init__(self, objectified_concentrator, report_version, request_id,
                 report_type):
        """

        """
        super(ConcentratorS15, self).__init__(objectified_concentrator,
                                              report_version, request_id)
        self.report_version = report_version
        self.request_id = request_id
        self.report_type = report_type

    @property
    def parameters(self):
        """
        Parameter set objects of this concentrator.

        :return: a list of parameter set objects
        """
        parameters = []
        if getattr(self.objectified, 'S15', None) is not None:
            for parameter in self.objectified.S15:
                parameters.append(ParameterConcentratorEvents(
                    parameter,
                    self.report_version,
                    self.name,
                    self.request_id))
        return parameters


class ConcentratorS17(ConcentratorEvents):

    def __init__(self, objectified_concentrator, report_version, request_id,
                 report_type):
        """

        """
        super(ConcentratorS17, self).__init__(objectified_concentrator,
                                              report_version, request_id)
        self.report_version = report_version
        self.request_id = request_id
        self.report_type = report_type

    @property
    def parameters(self):
        """
        Parameter set objects of this concentrator.

        :return: a list of parameter set objects
        """
        parameters = []
        if getattr(self.objectified, 'S17', None) is not None:
            for parameter in self.objectified.S17:
                parameters.append(ParameterConcentratorEvents(
                    parameter,
                    self.report_version,
                    self.name,
                    self.request_id))
        return parameters


class MeasureS18(MeasureActiveReactive):
    """
    Class for a set of measures of report S18.
    """
    @property
    def values(self):
        """
        Set of measures of report S18.
        :return: a dict with a set of measures of report S18.
        """
        values = {}
        try:
            get = self.objectified.get
            values.update({
                'order_datetime': self._get_timestamp('Fh'),
                'orden': get_integer_value(get('Orden')),
            })

        except Exception as e:
            self._warnings.append('ERROR: Thrown exception: {}'.format(e))
            return []
        return [values]


class MeterS18(MeterWithMagnitude):
    """
    Class for a meter of report S18.
    """

    @property
    def report_type(self):
        """
        The type of report for report S18.

        :return: a string with 'S18'
        """
        return 'S18'

    @property
    def measure_class(self):
        """
        The class used to instance measure sets for report S18.

        :return: a class to instance measure sets of report S18
        """
        return MeasureS18


class ConcentratorS18(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a set of measures of report S18.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S18.

        :return: a class to instance meters of report S18
        """
        return MeterS18


class ConcentratorS21(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S01.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S21.

        :return: a class to instance meters of report S21
        """
        return MeterS21


class ConcentratorS23(ConcentratorWithMetersWithConcentratorName):

    """
    Class for a concentrator of report S23.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S23.

        :return: a class to instance meters of report S23
        """
        return MeterS23

    @property
    def values(self):
        """
        Values of the set of parameters of this concentrator.

        :return: a list with the values of the meters
        """
        values = []
        for parameter in self.parameters:
            values.append(parameter.values)
            self._warnings.extend(parameter.warnings)
        return values

class ConcentratorS24(Concentrator):
    """
        Class for a concentrator of report S24.
    """

    def __init__(self, objectified_concentrator, report_version, request_id,
                 report_type):
        """

        """
        super(ConcentratorS24, self).__init__(objectified_concentrator)
        self.report_version = report_version
        self.request_id = request_id
        self.report_type = report_type

    @property
    def parameters(self):
        """
        Parameter set objects of this concentrator.

        :return: a list of parameter set objects
        """
        parameters = []
        if getattr(self.objectified, 'S24', None) is not None:
            for parameter in self.objectified.S24:
                parameters.append(ParameterS24(
                    parameter,
                    self.report_version,
                    self.name,
                    self.request_id))
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
            self._warnings.extend(parameter.warnings)
        return values


class ConcentratorS42(ConcentratorWithMetersWithConcentratorName):
    """
    Class for a concentrator of report S42.
    """

    @property
    def meter_class(self):
        """
        The class used to instance meters for report S42.

        :return: a class to instance meters of report S42
        """
        return MeterS42


class RemoteTerminalUnitS52(RemoteTerminalUnitDetails):
    """
    Class for a remote terminal unit of report S52.
    """

    def __init__(self, objectified_rt_unit, report_version, request_id):
        """
        Create a RemoteTerminalUnit object for the report S52.

        :param objectified_rt_unit: an lxml.objectify.StringElement \
            representing a line supervisor
        :param report_version: a string with the version of report
        :return: a LineSupervisor object
        """
        super(RemoteTerminalUnitS52, self).__init__(objectified_rt_unit)
        self.report_version = report_version
        self.request_id = request_id

    @property
    def line_supervisor_class(self):
        """
        The class used to instance line supervisors for report S52.

        :return: a class to instance line supervisors of report S52
        """
        return LineSupervisorS52

    @property
    def report_type(self):
        """
        The type of report for report S52.
        :return: a string with 'S52'
        """
        return 'S52'


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
        if hasattr(value, 'read') or isinstance(value, str):
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
            'S01': {
                'class': ConcentratorS01,
                'args': [objectified_concentrator]
            },
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
            'S09': {
                'class': ConcentratorS09,
                'args': [objectified_concentrator]
            },
            'S12': {
                'class': ConcentratorS12,
                'args': [objectified_concentrator, self.report_version]
            },
            'S13': {
                'class': ConcentratorS13,
                'args': [objectified_concentrator]
            },
            'S14': {
                'class': ConcentratorS14,
                'args': [objectified_concentrator]
            },
            'S15': {
                'class': ConcentratorS15,
                'args': [
                    objectified_concentrator,
                    self.report_version,
                    self.request_id,
                    self.report_type
                ]
            },
            'S17': {
                'class': ConcentratorS17,
                'args': [
                    objectified_concentrator,
                    self.report_version,
                    self.request_id,
                    self.report_type
                ]
            },
            'S18': {
                'class': ConcentratorS18,
                'args': [objectified_concentrator]
            },
            'S21': {
                'class': ConcentratorS21,
                'args': [objectified_concentrator]
            },
            'S23': {
                'class': ConcentratorS23,
                'args': [objectified_concentrator]
            },
            'S24': {
                'class': ConcentratorS24,
                'args': [
                    objectified_concentrator,
                    self.report_version,
                    self.request_id,
                    self.report_type
                ]
            },
            'S27': {
                'class': ConcentratorS27,
                'args': [objectified_concentrator]
            },
            'S42': {
                'class': ConcentratorS42,
                'args': [objectified_concentrator]
            }
        }

        if self.report_type not in report_type_class:
            raise NotImplementedError('Report type not implemented!')

        get = report_type_class.get(self.report_type).get
        concentrator_class = get('class')
        concentrator_args = get('args')
        concentrator = concentrator_class(*concentrator_args)
        return concentrator

    def get_rt_unit(self, objectified_rt_unit):
        """
        Instances a remote terminal unit object

        :return: a remote terminal unit object
        """
        report_type_class = {
            'S52': {
                'class': RemoteTerminalUnitS52,
                'args': [
                    objectified_rt_unit,
                    self.report_version,
                    self.request_id
                ],
            }
        }

        if self.report_type not in report_type_class:
            raise NotImplementedError('Report type not implemented!')

        get = report_type_class.get(self.report_type).get
        rt_unit_class = get('class')
        rt_unit_args = get('args')
        rt_unit = rt_unit_class(*rt_unit_args)
        return rt_unit

    @property
    def supported(self):
        return is_supported(self.report_type)

    @property
    def concentrators(self):
        """
        The concentrators of the report.

        :return: a list of concentrators of the report
        """
        return map(self.get_concentrator, self.message.objectified.Cnc)

    @property
    def rt_units(self):
        """
        The remote terminal units of the report.

        :return: a list of remote terminals units of the report
        """
        return map(self.get_rt_unit, self.message.objectified.Rtu)

    @property
    def values(self):
        """
        Values of the whole report.

        :return: a list with the values of the whole report
        """
        values = []
        if self.report_type == 'S52':
            for rt_unit in self.rt_units:
                values.extend(rt_unit.values)
        else:
            for concentrator in self.concentrators:
                values.extend(concentrator.values)
        return values
