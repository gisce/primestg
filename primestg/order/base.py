from libcomxml.core import XmlModel, XmlField


class Order(XmlModel):
    _sort_order = ('order', 'cnc')

    def __init__(self, id_pet, b_order, cnc):
        self.order = XmlField('Order', attributes={
                'IdPet': str(id_pet),
                'IdReq': b_order,
                'Version': '3.1.c'
        })
        self.cnc = Cnc(cnc)
        super(Order, self).__init__('Order', 'order')


class Cnc(XmlModel):
    def __init__(self, cnc, drop_empty=False):
        self.cnc = XmlField('Cnc', attributes={
                 'Id': cnc
        })
        self.payload = None
        super(Cnc, self).__init__('Cnc', 'cnc', drop_empty=drop_empty)
