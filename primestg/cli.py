## -*- encoding: utf-8 -*-
from __future__ import absolute_import
import sys                                                                      
import click
from datetime import datetime, timedelta
from pytz import timezone
from primestg.ziv_service import ZivService
import base64

TZ = timezone('Europe/Madrid')

from primestg.service import Service, format_timestamp
from primestg.contract_templates import CONTRACT_TEMPLATES
from primestg.utils import DLMSTemplates


REPORTS = [
    'get_instant_data',
    'get_advanced_instant_data',
    'get_meter_parameters',
    'get_concentrator_parameters',
]

ORDERS = {
    # CUTOFF
    'cutoff': {'order': 'B03', 'func': 'get_cutoff_reconnection'},
    'reconnect': {'order': 'B03', 'func': 'get_cutoff_reconnection'},
    'connect': {'order': 'B03', 'func': 'get_cutoff_reconnection'},
    # CONTRACT
    'contract': {'order': 'B04', 'func': 'get_contract'},
    'powers': {'order': 'B02', 'func': 'get_powers'},
    'dlms': {'order': 'B12', 'func': 'order_raw_dlms'},
    # CNC config
    'cnc_ftpip': {'order': 'B07', 'func': 'set_concentrator_ipftp'}
}


def get_meter_cnc_name(param):
    if '@' in param:
        meter, cnc = param.split('@')
    else:
        meter = param
        cnc = 'ZIV0004394488'
    return meter, cnc


def get_id_pet():
    now = datetime.now()
    return (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    ).seconds

@click.group(name="primestg")
def primestg(**kwargs):
    pass


# Gets a specific report by name
@primestg.command(name='report')                                                       
@click.argument('report_name', type=click.Choice(REPORTS),
                required=True
)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080/WS_DC/WS_DC.asmx"
)   
@click.option("--meter", "-m", default="ZIV0040318130")
def get_sync_report(**kwargs):
    """Gets sync report"""
    id_pet = get_id_pet()
    s = Service(id_pet, kwargs['cnc_url'], sync=True)
    func = getattr(s, kwargs['report_name'])
    try:
        res = func(kwargs['meter'])
    except:
        res = func(kwargs['meter'], '2019-01-01 00:00:00', '2019-01-01 00:00:00')
    print(res)


# Gets a raw report
@primestg.command(name='get_raw')
@click.argument('sxx', required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080/WS_DC/WS_DC.asmx"
)   
@click.option("--meter", "-m", default="ZIV0040318130")
@click.option(
    "--async", "-a", is_flag=True,
    help="Sends an Async Petition to send report to FTP"
)
def get_sync_sxx(**kwargs):
   """Get raw Sxx report"""
   sync = not kwargs['async']
   id_pet = get_id_pet()
   s = Service(id_pet, kwargs['cnc_url'], sync=sync, source='DCF')
   meter_name, cnc_name = get_meter_cnc_name(kwargs['meter'])
   res = s.send(kwargs['sxx'],meter_name)
   print(res)


# Sends an order
@primestg.command(name='order')
@click.argument('order', type=click.Choice(ORDERS), required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080/WS_DC/WS_DC.asmx"
)   
@click.option("--version", "-v", default="3.1.c")
@click.option("--meter", "-m", default="ZIV0040318130")
@click.option("--contract", "-c", default="1")
@click.option("--tariff", "-t", default="2.0_ST", help="One of available templates (see primestg templates or dlms_cycles)")
@click.option("--activation_date", "-d", default="2021-04-01 00:00:00")
@click.option("--powers", "-p", default="15000,15000,15000,15000,15000,15000",
              help='comma separated orders list of 6 powers'
)
@click.option("--ip", "-i", default="10.26.0.4", help='IP i.e CNC FTPIp')
def sends_order(**kwargs):
   """Sends on of available Orders to Meter or CNC"""
   id_pet = get_id_pet()
   s = Service(id_pet, kwargs['cnc_url'], sync=True)
   order_name = kwargs['order']
   order_code = ORDERS[order_name]['order']
   meter_name, cnc_name = get_meter_cnc_name(kwargs['meter'])
   version = kwargs['version']
   generic_values = {
       'id_pet': id_pet,
       'id_req': order_code,
       'cnc': cnc_name,
       'cnt': meter_name,
       'version': version,
   }
   vals = {}
   if order_name == 'cutoff':
       vals = {
           'order_param': '0',
       }
   elif order_name == 'reconnect':
       vals = {
           'order_param': '1'
       }
   elif order_name == 'connect':
       vals = {
           'order_param': '2'
       }
   elif order_name == 'contract':
       vals = {
           'contract': kwargs['contract'],
           'name': kwargs['tariff'],
           'activation_date': TZ.localize(
               datetime.strptime(kwargs['activation_date'], '%Y-%m-%d %H:%M:%S')
           )
       }
   elif order_name == 'powers':
       vals = {
           'powers': kwargs['powers'].split(','),
           'activation_date': TZ.localize(
               datetime.strptime(kwargs['activation_date'], '%Y-%m-%d %H:%M:%S')
           )
       }
   elif order_name == 'dlms':
       try:
           # datetime
           activation_date = (datetime.strptime(kwargs['activation_date'], '%Y-%m-%d %H:%M:%S')).date()
       except Exception as e:
           # date
           activation_date = (datetime.strptime(kwargs['activation_date'], '%Y-%m-%d')).date()

       vals = {
           'template': kwargs['tariff'],
           'powers': kwargs['powers'].split(','),
           'date': activation_date,
       }
   elif order_name == 'cnc_ftpip':
       vals = {
           'IPftp': kwargs['ip']
       }

   vals.update({
       'date_to': format_timestamp(datetime.now()+timedelta(hours=1)),
       'date_from': format_timestamp(datetime.now()),
   })

   func = getattr(s, ORDERS[order_name]['func'])
   res = func(generic_values, vals)
   print(res)


# Sends a CNC Txx order (B11)
@primestg.command(name='cnc_control')
@click.argument('order',required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080/WS_DC/WS_DC.asmx"
)
@click.option("--version", "-v", default="3.1.c")
@click.option("--meter", "-m", default="@ZIV0004394488")
def cnc_control(**kwargs):
   """Sends a TXX order to CNC"""
   id_pet = get_id_pet()
   s = Service(id_pet, kwargs['cnc_url'], sync=True)
   meter_name, cnc_name = get_meter_cnc_name(kwargs['meter'])
   version = kwargs['version']
   generic_values = {
       'id_pet': id_pet,
       'id_req': 'B11',
       'cnc': cnc_name,
       'version': version
   }
   vals = {
       'txx': kwargs['order'],
       'date_from': format_timestamp(datetime.now()),
       'date_to': format_timestamp(datetime.now())
   }
   res = s.get_order_request(generic_values, vals)
   print(res)


# Gets available contract templates
@primestg.command(name='templates')
def get_contract_templates(**kwargs):
    """Available contract templates for B04 order"""
    print('# Available contract templates for B04 order:\n')
    for name in sorted(CONTRACT_TEMPLATES.keys()):
        data = CONTRACT_TEMPLATES[name]
        print(' * {}: {}'.format(name, data['description']))


@primestg.command(name='dlms_cycles')
def get_dlms_cycles(**kwargs):
    """Available DLMS cycles for B12 a.k.a dlms order"""
    print('# Available DLMS cycles for B12 a.k.a dlms order:\n')
    dt = DLMSTemplates()
    templates = dt.get_available_templates()
    for name in sorted([t[0] for t in templates]):
        data = dt.get_template(name)
        params_txt = data['params'] and '.requires {}'.format(','.join(data['params'])) or ''
        print(' * {}: {}'.format(name, data['description'], params_txt))

@primestg.command(name='ziv_cycle')
@click.argument('cnc_url',required=True)
@click.argument('filename',required=True)
@click.argument('user',required=True)
@click.argument('password',required=True)
def send_ziv_cycle(**kwargs):
    """Sends a cycle to a ZIV CNC"""
    zs = ZivService(kwargs['cnc_url'], user=kwargs['user'], password=kwargs['password'], sync=True)
    content = base64.b64encode(open(kwargs['filename'],'rb').read())
    result = zs.send_cycle(filename=kwargs['filename'], cycle_filedata=content)
    print(result.content)

if __name__ == 'main':
    primestg()
