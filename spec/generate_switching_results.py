from switching.input.messages.TG import Concentrator, Values
from switching.input.messages.message import MessageTG

data = [
    'data/CIR4621247027_0_S02_0_20150901111051',
    'data/CIR4621247027_0_S04_0_20150901110412',
    'data/CIR4621247027_0_S05_0_20150901072044',
    'data/CIR4621247027_0_S12_0_20150903140000'
]

for filename in data:

    with open(filename) as data_file:
        message_tg = MessageTG(data_file)
    message_tg.parse_xml()
    type = message_tg.get_tipus_xml()
    concentrator = Concentrator(message_tg.obj.Cnc[0])

    result = []
    if concentrator.has_meters:
        for meter in concentrator.get_meters():
            result.append(Values(meter, type, concentrator).get())
    else:
        result.append(Values(concentrator, type, concentrator).get())

    with open('{}_result.txt'.format(filename), 'w') as result_file:
        result_file.write(str(result))