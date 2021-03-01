from ast import literal_eval

from expects import expect, equal
from primestg.report import Report


with description('Report S23 examples'):
    with before.all:

        self.data_filenames = [
            'spec/data/ZIV0004488684_59412C2_S23_0_20190424225341',
            # File with supervisor
            'spec/data/CIR4621816077_59864AC_S23_0_20190514165558'
        ]

        self.report = []
        for data_filename in self.data_filenames:
            with open(data_filename) as data_file:
                self.report.append(Report(data_file))

    with it('generates expected results for the values of the first pcact of the first concentrator'):

        expected_first_meter_values = \
            [
                {
                    "date": "2019-04-24 22:52:21",
                    "latent_calendars": {
                        "contracts": [
                            {
                                "is_active_calendar": False,
                                "c": "1",
                                "days": [
                                    {
                                        "day_id": "01",
                                        "changes": [
                                            {
                                                "tariffrate": "0001",
                                                "hour": 13
                                            },
                                            {
                                                "tariffrate": "0002",
                                                "hour": 23
                                            }
                                        ]
                                    },
                                    {
                                        "day_id": "02",
                                        "changes": [
                                            {
                                                "tariffrate": "0001",
                                                "hour": 12
                                            },
                                            {
                                                "tariffrate": "0002",
                                                "hour": 22
                                            }
                                        ]
                                    }
                                ],
                                "seasons": [
                                    {
                                        "week": "01",
                                        "start": "FFFFFEFFFFFFFF0000800080",
                                        "name": "01"
                                    },
                                    {
                                        "week": "02",
                                        "start": "FFFFFDFFFFFFFF0000800000",
                                        "name": "02"
                                    }
                                ],
                                "weeks": [
                                    {
                                        "week": "01010101010101",
                                        "index": 0,
                                        "name": "01",
                                        "day6": "01",
                                        "day4": "01",
                                        "day5": "01",
                                        "day2": "01",
                                        "day3": "01",
                                        "day0": "01",
                                        "day1": "01"
                                    },
                                    {
                                        "week": "02020202020202",
                                        "index": 1,
                                        "name": "02",
                                        "day6": "02",
                                        "day4": "02",
                                        "day5": "02",
                                        "day2": "02",
                                        "day3": "02",
                                        "day0": "02",
                                        "day1": "02"
                                    }
                                ],
                                "calendar_type": "01",
                                "calendar_name": "2.0DHA",
                                "act_date": "1900-01-01 00:00:00"
                            },
                            {
                                "is_active_calendar": False,
                                "c": "2",
                                "calendar_type": "01",
                                "calendar_name": "      ",
                                "act_date": "1900-01-01 00:00:00"
                            },
                            {
                                "is_active_calendar": False,
                                "c": "3",
                                "calendar_type": "01",
                                "calendar_name": "      ",
                                "act_date": "1900-01-01 00:00:00"
                            }
                        ]
                    },
                    "pc_act": {
                        "contrato1": {
                            "tr1": 55000,
                            "tr3": 55000,
                            "tr2": 55000,
                            "tr5": 55000,
                            "tr4": 55000,
                            "tr6": 55000
                        },
                        "act_date": "2018-03-06 15:26:21"
                    },
                    "pc_latent": {
                        "contrato1": {
                            "tr1": 55000,
                            "tr3": 55000,
                            "tr2": 55000,
                            "tr5": 55000,
                            "tr4": 55000,
                            "tr6": 55000
                        },
                        "act_date": "1900-01-01 00:00:00"
                    },
                    "active_calendars": {
                        "contracts": [
                            {
                                "is_active_calendar": True,
                                "c": "1",
                                "days": [
                                    {
                                        "day_id": "01",
                                        "changes": [
                                            {
                                                "tariffrate": "0001",
                                                "hour": 13
                                            },
                                            {
                                                "tariffrate": "0002",
                                                "hour": 23
                                            }
                                        ]
                                    },
                                    {
                                        "day_id": "02",
                                        "changes": [
                                            {
                                                "tariffrate": "0001",
                                                "hour": 12
                                            },
                                            {
                                                "tariffrate": "0002",
                                                "hour": 22
                                            }
                                        ]
                                    }
                                ],
                                "special_days": [
                                    {
                                        "day_id": "01",
                                        "dt": {
                                            "timestamp": "2011-12-25 00:00:00",
                                            "month": 12,
                                            "day": 25,
                                            "year": 2011
                                        },
                                        "dt_card": False
                                    },
                                    {
                                        "day_id": "01",
                                        "dt": {
                                            "timestamp": "2011-08-15 00:00:00",
                                            "month": 8,
                                            "day": 15,
                                            "year": 2011
                                        },
                                        "dt_card": False
                                    },
                                    {
                                        "day_id": "01",
                                        "dt": {
                                            "timestamp": "2011-07-14 00:00:00",
                                            "month": 7,
                                            "day": 14,
                                            "year": 2011
                                        },
                                        "dt_card": False
                                    },
                                    {
                                        "day_id": "01",
                                        "dt": {
                                            "timestamp": "2011-05-01 00:00:00",
                                            "month": 5,
                                            "day": 1,
                                            "year": 2011
                                        },
                                        "dt_card": False
                                    }
                                ],
                                "seasons": [
                                    {
                                        "week": "01",
                                        "start": "FFFFFEFFFFFFFF0000800080",
                                        "name": "01"
                                    },
                                    {
                                        "week": "02",
                                        "start": "FFFFFDFFFFFFFF0000800000",
                                        "name": "02"
                                    }
                                ],
                                "weeks": [
                                    {
                                        "week": "01010101010101",
                                        "index": 0,
                                        "name": "01",
                                        "day6": "01",
                                        "day4": "01",
                                        "day5": "01",
                                        "day2": "01",
                                        "day3": "01",
                                        "day0": "01",
                                        "day1": "01"
                                    },
                                    {
                                        "week": "02020202020202",
                                        "index": 1,
                                        "name": "02",
                                        "day6": "02",
                                        "day4": "02",
                                        "day5": "02",
                                        "day2": "02",
                                        "day3": "02",
                                        "day0": "02",
                                        "day1": "02"
                                    }
                                ],
                                "calendar_type": "01",
                                "calendar_name": "2.0DHA",
                                "act_date": "2018-03-06 15:26:21"
                            },
                            {
                                "is_active_calendar": True,
                                "c": "2",
                                "calendar_type": "01",
                                "calendar_name": "      ",
                                "act_date": "1900-01-01 00:00:00"
                            },
                            {
                                "is_active_calendar": True,
                                "c": "3",
                                "calendar_type": "01",
                                "calendar_name": "      ",
                                "act_date": "1900-01-01 00:00:00"
                            }
                        ]
                    }
                }
            ]

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

    with it('With hexadecimal datetime report'):
        with open('spec/data/ZIV0004389874_7_S23_0_20210226020937') as data_file:
            report = Report(data_file)
            print report.concentrators[0].meters[0].values[0].get('latent_calendars').get('contracts')[0].get('act_date')
            expect('2021-04-01 04:00:00').to(
                equal(report.concentrators[0].meters[0].values[0].get('latent_calendars').get('contracts')[0].get(
                    'act_date')))
