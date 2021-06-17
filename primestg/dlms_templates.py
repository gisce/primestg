# -*- coding: utf-8 -*-

DLMS_TEMPLATES = {
    # CONTRACTS
    'TAR_20TD': {
        'description': '3T_TDA - 2.0TD 3 periods and and special days. LATENT c1 Activation on selected date',
        'origin': 'library',
        'category': 'contract',
        'params': [],
        'data':  [
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "7", 'data': "raw{{01010203090101090cffff0101ff00000000800000090101}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "8", 'data': "raw{{010102080901011101110111011101110111021102}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "9", 'data': "raw{{0102020211010106020309040000000009060100003001ff120003020309040800000009060100003001ff120002020309040a00000009060100003001ff120001020309040e00000009060100003001ff120002020309041200000009060100003001ff120001020309041600000009060100003001ff120002020211020101020309040000000009060100003001ff120003}}"},
            {'obis': "0.0.11.0.4.255", 'class': "11", 'element': "2", 'data': "raw{{010902031200010905FFFF0101FF110202031200080905FFFF0106FF110202031200020905FFFF0501FF110202031200030905FFFF080FFF110202031200040905FFFF0A0CFF110202031200050905FFFF0B01FF110202031200060905FFFF0C06FF110202031200070905FFFF0C08FF110202031200080905FFFF0C19FF1102}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "10", 'data': "raw{{090C{date}FF000000000800FF}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "6", 'data': "raw{{090633545F544441}}"},
        ],
    },
    'TAR_30TD': {
        'description': '6T_TDA - 3.0TD with seasons and special days. LATENT c1 Activation on selected date',
        'origin': 'library',
        'category': 'contract',
        'params': [],
        'data': [
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "7", 'data': "raw{{01090203090101090cffff0101ff000000008000000901010203090102090cffff0301ff000000008000000901020203090103090cffff0401ff000000008000000901030203090104090cffff0601ff000000008000000901040203090105090cffff0701ff000000008000000901010203090106090cffff0801ff000000008000000901040203090107090cffff0a01ff000000008000000901030203090108090cffff0b01ff000000008000000901020203090109090cffff0c01ff00000000800000090101}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "8", 'data': "raw{{010402080901011101110111011101110111051105020809010211021102110211021102110511050208090103110411041104110411041105110502080901041103110311031103110311051105}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "9", 'data': "raw{{0105020211010106020309040000000009060100003001ff120006020309040800000009060100003001ff120002020309040900000009060100003001ff120001020309040e00000009060100003001ff120002020309041200000009060100003001ff120001020309041600000009060100003001ff120002020211020106020309040000000009060100003001ff120006020309040800000009060100003001ff120003020309040900000009060100003001ff120002020309040e00000009060100003001ff120003020309041200000009060100003001ff120002020309041600000009060100003001ff120003020211030106020309040000000009060100003001ff120006020309040800000009060100003001ff120004020309040900000009060100003001ff120003020309040e00000009060100003001ff120004020309041200000009060100003001ff120003020309041600000009060100003001ff120004020211040106020309040000000009060100003001ff120006020309040800000009060100003001ff120005020309040900000009060100003001ff120004020309040e00000009060100003001ff120005020309041200000009060100003001ff120004020309041600000009060100003001ff120005020211050101020309040000000009060100003001ff120006}}"},
            {'obis': "0.0.11.0.4.255", 'class': "11", 'element': "2", 'data': "raw{{010902031200010905FFFF0101FF110502031200080905FFFF0106FF110502031200020905FFFF0501FF110502031200030905FFFF080FFF110502031200040905FFFF0A0CFF110502031200050905FFFF0B01FF110502031200060905FFFF0C06FF110502031200070905FFFF0C08FF110502031200080905FFFF0C19FF1105}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "10", 'data': "raw{{090C{date}FF000000000800FF}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "6", 'data': "raw{{090636545F544441}}"},
        ],
    },
    # POWERS
    'C1_LAT_POWERS': {
        'description': 'Set powers on LATENT c1. Ordered power list p1,p2,p3,p4,p5,p6 and date.',
        'origin': 'library',
        'category': 'powers',
        'params': ['powers', 'date'],
        'data': [
            {'obis': "0.1.94.34.11.255", 'class': "3", 'element': "2", 'data': "raw{{06{p1}}}"},
            {'obis': "0.1.94.34.12.255", 'class': "3", 'element': "2", 'data': "raw{{06{p2}}}"},
            {'obis': "0.1.94.34.13.255", 'class': "3", 'element': "2", 'data': "raw{{06{p3}}}"},
            {'obis': "0.1.94.34.14.255", 'class': "3", 'element': "2", 'data': "raw{{06{p4}}}"},
            {'obis': "0.1.94.34.15.255", 'class': "3", 'element': "2", 'data': "raw{{06{p5}}}"},
            {'obis': "0.1.94.34.16.255", 'class': "3", 'element': "2", 'data':  "raw{{06{p6}}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "10", 'data': "raw{{090C{date}FF000000000800FF}}"},
        ],
    },
    'C1_ACT_POWERS': {
        'description': 'Set powers on ACTUAL c1. Ordered power list p1,p2,p3,p4,p5,p6',
        'origin': 'library',
        'category': 'powers',
        'params': ['powers'],
        'data': [
            {'obis': "0.1.94.34.11.255", 'class': "3", 'element': "2", 'data': "raw{{06{p1}}}"},
            {'obis': "0.1.94.34.12.255", 'class': "3", 'element': "2", 'data': "raw{{06{p2}}}"},
            {'obis': "0.1.94.34.13.255", 'class': "3", 'element': "2", 'data': "raw{{06{p3}}}"},
            {'obis': "0.1.94.34.14.255", 'class': "3", 'element': "2", 'data': "raw{{06{p4}}}"},
            {'obis': "0.1.94.34.15.255", 'class': "3", 'element': "2", 'data': "raw{{06{p5}}}"},
            {'obis': "0.1.94.34.16.255", 'class': "3", 'element': "2", 'data': "raw{{06{p6}}}"},
            {'obis': "0.0.13.0.1.255", 'class': "20", 'element': "10", 'data': "raw{{090C07D10101FF000000000800FF}}"},
        ],
    },
}
