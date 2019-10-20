## -*- encoding: utf-8 -*-                                                       
import sys                                                                      
import click
from datetime import datetime, timedelta

from primestg.service import Service, format_timestamp

REPORTS = [
    'get_instant_data',
    'get_advanced_instant_data',
    'get_meter_parameters',
    'get_concentrator_parameters',
]

ORDERS = [
    'cutoff',
    'reconnect',
    'connect'
]

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
                default="http://cct.gisce.lan:8080"
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
    print res


# Gets a raw report
@primestg.command(name='get_raw')
@click.argument('sxx', required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080"
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
   res = s.send(kwargs['sxx'],kwargs['meter'])
   print res

# Sends an order
@primestg.command(name='order')
@click.argument('order', type=click.Choice(ORDERS), required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080"
)   
@click.option("--meter", "-m", default="ZIV0040318130")
def sends_order(**kwargs):
   id_pet = get_id_pet()
   s = Service(id_pet, kwargs['cnc_url'], sync=True)
   generic_values = {
       'id_pet': id_pet,
       'id_req': 'B03',
       'cnc': 'ZIV0004394488',
       'cnt': kwargs['meter'],
   }
   if kwargs['order'] == 'cutoff':
       vals = {
           'order_param': '0',
       }
   elif kwargs['order'] == 'reconnect':
       vals = {
           'order_param': '1'
       }
   elif kwargs['order'] == 'connect':
       vals = {
           'order_param': '2'
       }
   vals.update({
       'date_to': format_timestamp(datetime.now()+timedelta(hours=1)),
       'date_from': format_timestamp(datetime.now()),
   })

   res = s.get_cutoff_reconnection(generic_values, vals)
   print res

# Sends a CNC Txx order (B11)
@primestg.command(name='cnc_control')
@click.argument('order',required=True)
@click.argument("cnc_url", required=True,
                default="http://cct.gisce.lan:8080"
)   
def cnc_control(**kwargs):
   id_pet = get_id_pet()
   s = Service(id_pet, kwargs['cnc_url'], sync=True)
   generic_values = {
       'id_pet': id_pet,
       'id_req': 'B11',
       'cnc': 'ZIV0004394488',
   }
   vals = {
       'txx': kwargs['order'],
       'date_from': format_timestamp(datetime.now()),
       'date_to': format_timestamp(datetime.now())
   }
   res = s.get_order_request(generic_values, vals)
   print res

if __name__ == 'main':
    primestg()
