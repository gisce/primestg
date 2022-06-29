from libcomxml.core import XmlModel, XmlField


class OrderHeader(XmlModel):
    _sort_order = ('order', 'cnc')

    def __init__(self, id_pet, b_order, cnc, version='3.1.c'):
        self.order = XmlField('Order', attributes={
                'IdPet': str(id_pet),
                'IdReq': b_order,
                'Version': version
        })
        self.cnc = Cnc(cnc)
        super(OrderHeader, self).__init__('Order', 'order')


class Cnc(XmlModel):
    def __init__(self, cnc, drop_empty=False):
        self.cnc = XmlField('Cnc', attributes={
                 'Id': cnc
        })
        self.payload = None
        super(Cnc, self).__init__('Cnc', 'cnc', drop_empty=drop_empty)


class CntOrderHeader(XmlModel):
    _sort_order = ('order', 'cnc')

    def __init__(self, id_pet, b_order, cnc, cnt, version='3.1.c'):
        self.order = XmlField('Order', attributes={
                'IdPet': str(id_pet),
                'IdReq': b_order,
                'Version': version
        })
        self.cnc = CncWithCnt(cnc, cnt)
        super(CntOrderHeader, self).__init__('Order', 'order')


class CncWithCnt(XmlModel):
    def __init__(self, cnc, cnt, drop_empty=False):
        self.cnc = XmlField('Cnc', attributes={
                 'Id': cnc
        })
        self.cnt = Cnt(cnt)
        super(CncWithCnt, self).__init__('Cnc', 'cnc', drop_empty=drop_empty)


class Cnt(XmlModel):
    def __init__(self, cnt, drop_empty=False):
        self.cnt = XmlField('Cnt', attributes={
                 'Id': cnt
        })
        self.payload = None
        super(Cnt, self).__init__('Cnt', 'cnt', drop_empty=drop_empty)


class LVSLine(XmlModel):
    def __init__(self, line_supervisor, drop_empty=False):
        self.cnt = XmlField('LVSLine', attributes={
                 'Id': line_supervisor
        })
        self.payload = None
        super(LVSLine, self).__init__('LVSLine', 'line_supervisor', drop_empty=drop_empty)
