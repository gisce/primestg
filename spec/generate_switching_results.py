from switching.input.messages.TG import Concentrator, Values
from switching.input.messages.message import MessageTG

data = [
    'data/CIR4621247027_0_S02_0_20150901111051',
    'data/CIR4621247027_0_S04_0_20150901110412',
    'data/CIR4621247027_0_S05_0_20150901072044',
    'data/CIR4621247027_0_S12_0_20150903140000',
    'data/ZIV0000034180_0_S09_0_20161216104003',
    'data/ZIV0000034180_0_S09_0_20161216090401',
    'data/ZIV0000034180_0_S09_0_20161216080308',
    'data/ZIV0000034180_0_S09_0_201612160empty',
    'data/ZIV0000035536_0_S15_0_20161204040002',
    'data/ZIV0000035545_0_S15_0_20161203040002',
    'data/ZIV0004311822_0_S15_0_20161215040002',
    'data/ZIV0000035536_0_S15_0_201612040empty',
    'data/ZIV0000034180_0_S13_0_20161216080308',
    'data/ZIV0000034180_0_S13_0_20161216090401',
    'data/ZIV0000034180_0_S13_0_20161216104003',
    'data/ZIV0000034180_0_S13_0_201612160empty',
    'data/ZIV0000035536_0_S17_0_20161204040002',
    'data/ZIV0000035545_0_S17_0_20161203040002',
    'data/ZIV0004311822_0_S17_0_20161215040002',
    'data/ZIV0000035536_0_S17_0_201612040empty',
]

for filename in data:

    with open(filename) as data_file:
        message_tg = MessageTG(data_file)
    message_tg.parse_xml()
    type = message_tg.get_tipus_xml()
    concentrator = Concentrator(message_tg.obj.Cnc[0])

    if concentrator.has_meters:
        result = []
        for meter in concentrator.get_meters():
            result.extend(Values(meter, type, concentrator).get())
    else:
        result = Values(concentrator, type, concentrator).get()

    with open('{}_result.txt'.format(filename), 'w') as result_file:
        result_file.write(str(result))
