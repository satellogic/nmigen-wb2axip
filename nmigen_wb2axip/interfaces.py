from nmigen.hdl.rec import DIR_FANOUT, DIR_FANIN, Record
from .layouts import get_axi_layout, get_axilite_layout


class AxiMaster(Record):
    def __init__(self, data_w, addr_w, id_w, user_w=0, **kargs):
        layout = get_axi_layout('master', data_w, addr_w, id_w, user_w)
        Record.__init__(self, layout, **kargs)

    def connect(self, slave):
        return connect_axi(self, slave)


class AxiSlave(Record):
    def __init__(self, data_w, addr_w, id_w, user_w=0, **kargs):
        layout = get_axi_layout('slave', data_w, addr_w, id_w, user_w)
        Record.__init__(self, layout, **kargs)

    def connect(self, master):
        return connect_axi(master, self)


class AxiLiteMaster(Record):
    def __init__(self, data_w, addr_w, **kargs):
        layout = get_axilite_layout('master', data_w, addr_w)
        Record.__init__(self, layout, **kargs)

    def connect(self, slave):
        return connect_axilite(self, slave)


class AxiLiteSlave(Record):
    def __init__(self, data_w, addr_w, **kargs):
        layout = get_axilite_layout('slave', data_w, addr_w)
        Record.__init__(self, layout, **kargs)

    def connect(self, master):
        return connect_axilite(master, self)


def _connect(master, slave):
    layout = [(k, v[1]) for k, v in master.layout.fields.items()]
    ret = [master[f].eq(slave[f]) for f, d in layout if d == DIR_FANIN]
    ret += [slave[f].eq(master[f]) for f, d in layout if d == DIR_FANOUT]
    return ret


def connect_axi(master, slave):
    assert isinstance(master, AxiMaster)
    assert isinstance(slave, AxiSlave)
    return _connect(master, slave)


def connect_axilite(master, slave):
    assert isinstance(master, AxiLiteMaster)
    assert isinstance(slave, AxiLiteSlave)
    return _connect(master, slave)
