# -*- coding: utf-8 -*-

CONTRACT_TEMPLATES = {
    '2.0_ST': {
        'description': '2.x 1 period contracts (Simple Tariff)',
        'origin': 'library',
        'type': '01',
        'seasons': [
            {
                'name': '01',
                'start': 'FFFFFEFFFFFFFF0000800080',
                'week': '01'
            }
        ],
        'weeks': [
            {
                'name': '01', 'week': '01010101010101'
            }
        ],
        'days': {
          '01': [{'hour': 1, 'period': 1}]
        }
    },
    'DHA_IT': {
        'description': '2.xDHA 2 period contracts (Double Tariff)',
        'origin': 'library',
        'type': '01',
        'seasons': [
          {
            'name': '01',
            'start': 'FFFFFEFFFFFFFF0000800080',
            'week': '01'
          },
          {
            'name': '02',
            'start': 'FFFFFDFFFFFFFF0000800000',
            'week': '02'
          }
        ],
        'weeks': [
          {
            'name': '01', 'week': '01010101010101'
          },
          {
            'name': '02', 'week': '02020202020202'
          }
        ],
        'days': {
            '01': [
                {'hour': 13, 'period': 1},
                {'hour': 23, 'period': 2}
            ],
            '02': [
                {'hour': 12, 'period': 1},
                {'hour': 22, 'period': 2}
            ]
        }
    },
    'DHS_IT': {
        'description': '2.xDHS 3 period contracts (Triple Tariff)',
        'origin': 'library',
        'type': '01',
        'seasons': [
            {
              'name': '01',
              'start': 'FFFFFEFFFFFFFF0000800080',
              'week': '01'
            },
            {
              'name': '02',
              'start': 'FFFFFDFFFFFFFF0000800000',
              'week': '02'
            }
        ],
        'weeks': [
            {
                'name': '01', 'week': '01010101010101'
            },
            {
                'name': '02', 'week': '02020202020202'
            }
        ],
        'days': {
            '01': [
                {'hour': 1, 'period': 3},
                {'hour': 7, 'period': 2},
                {'hour': 13, 'period': 23}
            ],
            '02': [
                {'hour': 1, 'period': 3},
                {'hour': 7, 'period': 2},
                {'hour': 13, 'period': 23}
            ]
        },
    },
    # 3/2020
    '2.0TDA': {
        'description': '2.0TDA 3 periods and special days',
        'origin': 'library',
        'type': '01',
        'seasons': [
            {
                'name': '01',
                'start': 'FFFF0101FF00000000800000',
                'week': '01'
            },
        ],
        'weeks': [
            {'name': '01', 'week': '01010101010202'}
        ],
        'days': {
            '01': [
                {'hour': 0, 'period': 3},
                {'hour': 8, 'period': 2},
                {'hour': 9, 'period': 1},
                {'hour': 14, 'period': 2},
                {'hour': 18, 'period': 1},
                {'hour': 22, 'period': 2}
            ],
            '02': [
                {'hour': 0, 'period': 3},
            ],
        },
        'special_days': [
            {'datetime': 'FFFF0101000000000W', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF0106000000000W', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF0501000000000S', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF0815000000000S', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF1012000000000S', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF1101000000000W', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF1206000000000W', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF1208000000000W', 'datetime_card': True, 'day_id': '03'},
            {'datetime': 'FFFF1225000000000W', 'datetime_card': True, 'day_id': '03'},
        ],
    },
    '3.0TDA': {
        'description': '3.0TDA with seasons and special days',
        'origin': 'library',
        'type': '01',
        'seasons': [
            {
                'name': '01',
                'start': 'FFFF0101FF00000000800000',
                'week': '01'
            },
            {
                'name': '02',
                'start': 'FFFF0301FF00000000800000',
                'week': '02'
            },
            {
                'name': '03',
                'start': 'FFFF0401FF00000000800000',
                'week': '03'
            },
            {
                'name': '04',
                'start': 'FFFF0601FF00000000800000',
                'week': '04'
            },
            {
                'name': '05',
                'start': 'FFFF0701FF00000000800000',
                'week': '01'
            },
            {
                'name': '06',
                'start': 'FFFF0801FF00000000800000',
                'week': '04'
            },
            {
                'name': '07',
                'start': 'FFFF0A01FF00000000800000',
                'week': '03'
            },
            {
                'name': '08',
                'start': 'FFFF0B01FF00000000800000',
                'week': '02'
            },
            {
                'name': '09',
                'start': 'FFFF0C01FF00000000800000',
                'week': '01'
            },
        ],
        'weeks': [
            {
                'name': '01', 'week': '01010101010505'
            },
            {
                'name': '02', 'week': '02020202020505'
            },
            {
                'name': '03', 'week': '04040404040505'
            },
            {
                'name': '04', 'week': '03030303030505'
            }
        ],
        'days': {
            '01': [
                {'hour': 0, 'period': 6},
                {'hour': 8, 'period': 2},
                {'hour': 9, 'period': 1},
                {'hour': 14, 'period': 2},
                {'hour': 18, 'period': 1},
                {'hour': 22, 'period': 2}
            ],
            '02': [
                {'hour': 0, 'period': 6},
                {'hour': 8, 'period': 3},
                {'hour': 9, 'period': 2},
                {'hour': 14, 'period': 3},
                {'hour': 18, 'period': 2},
                {'hour': 22, 'period': 3}
            ],
            '03': [
                {'hour': 0, 'period': 6},
                {'hour': 8, 'period': 4},
                {'hour': 9, 'period': 3},
                {'hour': 14, 'period': 4},
                {'hour': 18, 'period': 3},
                {'hour': 22, 'period': 4}
            ],
            '04': [
                {'hour': 0, 'period': 6},
                {'hour': 8, 'period': 5},
                {'hour': 9, 'period': 4},
                {'hour': 14, 'period': 5},
                {'hour': 18, 'period': 4},
                {'hour': 22, 'period': 5}
            ],
            '05': [
                {'hour': 0, 'period': 6},
            ]
        },
        'special_days': [
            {'datetime': 'FFFF0101000000000W', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF0106000000000W', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF0501000000000S', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF0815000000000S', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF1012000000000S', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF1101000000000W', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF1206000000000W', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF1208000000000W', 'datetime_card': True, 'day_id': '05'},
            {'datetime': 'FFFF1225000000000W', 'datetime_card': True, 'day_id': '05'},
        ]
    }
}
