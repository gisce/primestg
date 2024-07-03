# -*- coding: utf-8 -*-
from primestg.order.orders import Order
from primestg.utils import ContractTemplates, CONTRACT_TEMPLATES, datetimetoprime, octet2name, name2octet
from expects import expect, equal, contain, be_a, raise_error
from primestg.utils import assertXMLEqual
from datetime import datetime
from pytz import timezone

TZ = timezone('Europe/Madrid')


with description('Order B04 Generation'):

    with context('Support utilities'):

        with context('datetimetoprime: datetime to PRIME format'):

            with it('Generates a correct string from datetimes'):
                dates = [
                    (datetime(2020, 1, 1, 0), '20200101000000000W'),
                    (datetime(2020, 8, 1, 2, 3, 4), '20200801020304000S')
                ]

                for dt in dates:
                    expect(datetimetoprime(dt[0])).to(equal(dt[1]))
                    # localize
                    local_dt = TZ.normalize(TZ.localize(dt[0]))
                    expect(datetimetoprime(local_dt)).to(equal(dt[1]))

        with context('in Contract class'):

            with it('Contract.name2code converts string to octet string'):
                name = '6.1_TDA'
                octet = name2octet(name)
                new_name = octet2name(octet)
                expect(new_name).to(equal(name))

        with context('ContractTemplates class'):

            with before.all:
                self.ct = ContractTemplates()

            with it('may be instantiated'):
                expect(self.ct).to(be_a(ContractTemplates))

            with it('returns templates list'):
                templates = self.ct.get_available_templates()
                expect(len(templates)).to(equal(len(CONTRACT_TEMPLATES)))
                for tmpl in templates:
                    name, description, origin = tmpl
                    expect(CONTRACT_TEMPLATES.keys()).to(contain(name))
                    contract_tmpl = CONTRACT_TEMPLATES[name]
                    expect(contract_tmpl['description']).to(equal(description))
                    expect(contract_tmpl['origin']).to(equal(origin))

            with it('returns only selected library origin'):
                templates = self.ct.get_available_templates(origin='library')

                for tmpl in templates:
                    expect(tmpl[2]).to(equal('library'))

            with it('returns selected template'):
                for key, tmpl in CONTRACT_TEMPLATES.items():
                    template = self.ct.get_template(key)
                    expect(template['description']).to(equal(tmpl['description']))

            with it('raises Exception on inexistent template'):
                expect(lambda *a: self.ct.get_template('FAKE')).to(raise_error(KeyError))

    with describe('Generates B04'):
        with before.all:
            self.expected_result_20_ST = (
                """
                <Order IdPet="1234" IdReq="B04" Version="3.1.c">   
                    <Cnc Id="CIR000000000">
                        <Cnt Id="CNT000000000">
                            <B04>
                            <Contract c="1" CalendarType="01" CalendarName="322E305F5354" ActDate="{0}">
                                   <Season Name="01" Start="FFFFFEFFFFFFFF0000800080" Week="01"/>
                                   <Week Name="01" Week="01010101010101"/>
                                   <Day id="01">
                                     <Change Hour="01000000" TariffRate="0001"/>
                                   </Day>
                            </Contract>
                            </B04>
                        </Cnt>
                    </Cnc>
                </Order>
                """
            )
            self.expected_result_30TDA = (
                """
                <Order IdPet="1234" IdReq="B04" Version="3.1.c">   
                    <Cnc Id="CIR000000000">
                        <Cnt Id="CNT000000000">
                            <B04>
                                <Contract c="1" CalendarType="01" CalendarName="332E30544441" ActDate="{0}">
                                   <Season Name="01" Start="FFFF0101FF00000000800000" Week="01"/>
                                   <Season Name="02" Start="FFFF0301FF00000000800000" Week="02"/>
                                   <Season Name="03" Start="FFFF0401FF00000000800000" Week="03"/>
                                   <Season Name="04" Start="FFFF0601FF00000000800000" Week="04"/>
                                   <Season Name="05" Start="FFFF0701FF00000000800000" Week="01"/>
                                   <Season Name="06" Start="FFFF0801FF00000000800000" Week="04"/>
                                   <Season Name="07" Start="FFFF0A01FF00000000800000" Week="03"/>
                                   <Season Name="08" Start="FFFF0B01FF00000000800000" Week="02"/>
                                   <Season Name="09" Start="FFFF0C01FF00000000800000" Week="01"/>
                                   <Week Name="01" Week="01010101010505"/>
                                   <Week Name="02" Week="02020202020505"/>
                                   <Week Name="03" Week="04040404040505"/>
                                   <Week Name="04" Week="03030303030505"/>
                                   <Day id="01">
                                     <Change Hour="00000000" TariffRate="0006"/>
                                     <Change Hour="08000000" TariffRate="0002"/>
                                     <Change Hour="09000000" TariffRate="0001"/>
                                     <Change Hour="0E000000" TariffRate="0002"/>
                                     <Change Hour="12000000" TariffRate="0001"/>
                                     <Change Hour="16000000" TariffRate="0002"/>
                                   </Day>
                                   <Day id="02">
                                     <Change Hour="00000000" TariffRate="0006"/>
                                     <Change Hour="08000000" TariffRate="0003"/>
                                     <Change Hour="09000000" TariffRate="0002"/>
                                     <Change Hour="0E000000" TariffRate="0003"/>
                                     <Change Hour="12000000" TariffRate="0002"/>
                                     <Change Hour="16000000" TariffRate="0003"/>
                                   </Day>
                                   <Day id="03">
                                     <Change Hour="00000000" TariffRate="0006"/>
                                     <Change Hour="08000000" TariffRate="0004"/>
                                     <Change Hour="09000000" TariffRate="0003"/>
                                     <Change Hour="0E000000" TariffRate="0004"/>
                                     <Change Hour="12000000" TariffRate="0003"/>
                                     <Change Hour="16000000" TariffRate="0004"/>
                                   </Day>
                                   <Day id="04">
                                     <Change Hour="00000000" TariffRate="0006"/>
                                     <Change Hour="08000000" TariffRate="0005"/>
                                     <Change Hour="09000000" TariffRate="0004"/>
                                     <Change Hour="0E000000" TariffRate="0005"/>
                                     <Change Hour="12000000" TariffRate="0004"/>
                                     <Change Hour="16000000" TariffRate="0005"/>
                                   </Day>
                                   <Day id="05">
                                     <Change Hour="00000000" TariffRate="0006"/>
                                   </Day>
                                   <SpecialDays DT="FFFF0101000000000W" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF0106000000000W" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF0501000000000S" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF0815000000000S" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF1012000000000S" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF1101000000000W" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF1206000000000W" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF1208000000000W" DTCard="Y" DayID="05"/>
                                   <SpecialDays DT="FFFF1225000000000W" DTCard="Y" DayID="05"/>
                                </Contract>
                            </B04>
                        </Cnt>
                    </Cnc>
                </Order>
                """
            )
            self.expected_result_20TDA = (
                """
                <Order IdPet="1234" IdReq="B04" Version="3.1.c">   
                    <Cnc Id="CIR000000000">
                        <Cnt Id="CNT000000000">
                            <B04>
                                <Contract c="1" CalendarType="01" CalendarName="322E30544441" ActDate="{0}">
                                   <Season Name="01" Start="FFFF0101FF00000000800000" Week="01"/>
                                   <Week Name="01" Week="01010101010202"/>
                                   <Day id="01">
                                     <Change Hour="00000000" TariffRate="0003"/>
                                     <Change Hour="08000000" TariffRate="0002"/>
                                     <Change Hour="09000000" TariffRate="0001"/>
                                     <Change Hour="0E000000" TariffRate="0002"/>
                                     <Change Hour="12000000" TariffRate="0001"/>
                                     <Change Hour="16000000" TariffRate="0002"/>
                                   </Day>
                                   <Day id="02">
                                     <Change Hour="00000000" TariffRate="0003"/>
                                   </Day>
                                   <SpecialDays DT="FFFF0101000000000W" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF0106000000000W" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF0501000000000S" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF0815000000000S" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF1012000000000S" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF1101000000000W" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF1206000000000W" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF1208000000000W" DTCard="Y" DayID="03"/>
                                   <SpecialDays DT="FFFF1225000000000W" DTCard="Y" DayID="03"/>
                                </Contract>
                            </B04>
                        </Cnt>
                    </Cnc>
                </Order>
                """
            )
        with it('generates expected B04 xml with datetime as activation date'):

            activation_dates = [
                TZ.localize(datetime(2021, 4, 1, 0)),   # summer
                TZ.localize(datetime(2020, 11, 1, 0)),  # winter
                # not localized
                datetime(2021, 8, 1, 0),  # summer
                datetime(2020, 1, 1, 0),  # winter
             ]

            contracts = [
                ('2.0_ST', self.expected_result_20_ST),
                ('2.0TDA', self.expected_result_20TDA),
                ('3.0TDA', self.expected_result_30TDA),
            ]

            generic_values = {
                'id_pet': str(1234),
                'id_req': 'B04',
                'cnc': 'CIR000000000',
                'cnt': 'CNT000000000'
            }

            for contract_name, contract_template in contracts:
                for activation_date in activation_dates:
                    payload = {
                        'contract': 1,
                        'name': contract_name,
                        'activation_date': activation_date,
                    }

                    if activation_date.tzinfo is None:
                        season = TZ.normalize(TZ.localize(activation_date)).dst() and 'S' or 'W'
                    else:
                        season = activation_date.dst() and 'S' or 'W'

                    expected_activation_date = activation_date.strftime('%Y%m%d%H%M%S000{}'.format(season))
                    expected_result = contract_template.format(expected_activation_date)

                    order = Order('B04')
                    order = order.create(generic_values, payload)
                    assertXMLEqual(order, expected_result)