from ast import literal_eval

from expects import expect, equal
from primestg.report import Report


with description('Report S23 examples'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0004488684_59412C2_S23_0_20190424225341'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for the values of the first pcact of the first concentrator'):

        expected_first_meter_values = \
            [{
                'date': '2019-04-24 22:52:21',
                'latent_calendars': {
                    'c1': {
                        'calendar_type': '01',
                        'calendar_name': '322E30444841',
                        'act_date': '1900-01-01 00:00:00',
                        'seasons': {
                            'season1': {
                                'week': '01',
                                'start': 'FFFFFEFFFFFFFF0000800080',
                                'name': '01'
                            },
                            'season2': {
                                'week': '02',
                                'start': 'FFFFFDFFFFFFFF0000800000',
                                'name': '02'
                            }
                        },
                        'weeks': {
                            'week1': {
                                'week': '01010101010101',
                                'name': '01'
                            },
                            'week2': {
                                'week': '02020202020202',
                                'name': '02'
                            }
                        },
                        'days': {
                            'day1': {
                                'change1': {
                                    'hour': '0D000000',
                                    'tariffrate': '0001'
                                },
                                'change2': {
                                    'hour': '17000000',
                                    'tariffrate': '0002'
                                }
                            },
                            'day2': {
                                'change1': {
                                    'hour': '0C000000',
                                    'tariffrate': '0001'
                                },
                                'change2': {
                                    'hour': '16000000',
                                    'tariffrate': '0002'
                                }
                            }
                        }
                    },
                    'c2': {
                        'calendar_type': '01',
                        'calendar_name': '202020202020',
                        'act_date': '1900-01-01 00:00:00'
                    },
                    'c3': {
                        'calendar_type': '01',
                        'calendar_name': '202020202020',
                        'act_date': '1900-01-01 00:00:00'
                    }
                },
                'pc_act': {
                    'act_date': '2018-03-06 15:26:21',
                    'contrato1': {
                        'tr1': 55000,
                        'tr3': 55000,
                        'tr2': 55000,
                        'tr5': 55000,
                        'tr4': 55000,
                        'tr6': 55000
                    }
                },
                'pc_latent': {
                    'act_date': '1900-01-01 00:00:00',
                    'contrato1': {
                        'tr1': 55000,
                        'tr3': 55000,
                        'tr2': 55000,
                        'tr5': 55000,
                        'tr4': 55000,
                        'tr6': 55000
                    }
                },
                'active_calendars': {
                    'c1': {
                        'calendar_type': '01',
                        'calendar_name': '322E30444841',
                        'act_date': '2018-03-06 15:26:21',
                        'seasons': {
                            'season1': {
                                'name': '01',
                                'start': 'FFFFFEFFFFFFFF0000800080',
                                'week': '01'
                            },
                            'season2': {
                                'name': '02',
                                'start': 'FFFFFDFFFFFFFF0000800000',
                                'week': '02'
                            }
                        },
                        'weeks': {
                            'week1': {
                                'name': '01',
                                'week': '01010101010101'
                            },
                            'week2': {
                                'name': '02',
                                'week': '02020202020202'
                            }
                        },
                        'special_days': {
                            'special_day1': {
                                'day_id': '01',
                                'dt': '2011-12-25 00:00:00',
                                'dt_card': 'N'
                            },
                            'special_day2': {
                                'day_id': '01',
                                'dt': '2011-08-15 00:00:00',
                                'dt_card': 'N'
                            },
                            'special_day3': {
                                'day_id': '01',
                                'dt': '2011-07-14 00:00:00',
                                'dt_card': 'N'
                            },
                            'special_day4': {
                                'day_id': '01',
                                'dt': '2011-05-01 00:00:00',
                                'dt_card': 'N'
                            }
                        },
                        'days': {
                            'day1': {
                                'change1': {
                                    'hour': '0D000000',
                                    'tariffrate': '0001'
                                },
                                'change2': {
                                    'hour': '17000000',
                                    'tariffrate': '0002'
                                }
                            },
                            'day2': {
                                'change1': {
                                    'hour': '0C000000',
                                    'tariffrate': '0001'
                                },
                                'change2': {
                                    'hour': '16000000',
                                    'tariffrate': '0002'
                                }
                            }
                        }
                    },
                    'c2': {
                        'calendar_type': '01',
                        'calendar_name': '202020202020',
                        'act_date': '1900-01-01 00:00:00'
                    },
                    'c3': {
                        'calendar_type': '01',
                        'calendar_name': '202020202020',
                        'act_date': '1900-01-01 00:00:00'
                    }
                }
            }]

        #EXPECT1 CONCENTRATOR 0
        concentrator_name = list(self.report[0].concentrators)[0].name

        expect(concentrator_name) \
            .to(equal('ZIV0004488684'))

        #EXPECT2 METER 0
        meter_name = list(self.report[0].concentrators)[0].meters[0].name

        expect(meter_name) \
            .to(equal('ZIV0045682496'))

        #EXPECT3 METER 0 VALUES
        meter_values = list(self.report[0].concentrators)[0].meters[0].values

        expect(meter_values) \
            .to(equal(expected_first_meter_values))

    with it('generates the expected results for the whole report'):

        result_filenames = []
        warnings = []
        for data_filename in self.data_filenames:
            result_filenames.append('{}_result.txt'.format(data_filename))

        # with open(result_filename) as result_file:
        #     result_string = result_file.read()
        #     expected_result = literal_eval(result_string)

        for key, result_filename in enumerate(result_filenames):
            result = []
            with open(result_filename) as result_file:
                 result_string = result_file.read()
                 expected_result = literal_eval(result_string)
            for cnc in self.report[key].concentrators:
                if cnc.meters:
                    for meter in cnc.meters:
                        if meter.values:
                            for value in meter.values:
                                result.append(value)
                        if meter.warnings:
                            warnings.append(meter.warnings)

            expect(result).to(equal(expected_result))