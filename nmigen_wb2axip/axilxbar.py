from math import ceil, log2
from nmigen import *
from nmigen.build.plat import Platform
from .interfaces import AxiLiteSlave, AxiLiteMaster
from .utils import get_ports_for_instance, add_verilog_file

def length_to_mask(length, width):
    return (~int('1' * ceil(log2(length)), 2)) &  int('1' * width, 2)

class AxiLiteXBar(Elaboratable):
    DEPENDENCIES = ['axilxbar.v', 'addrdecode.v', 'skidbuffer.v']

    def __init__(self, data_w, addr_w, domain='sync'):
        self.domain = domain
        self.data_w = data_w
        self.addr_w = addr_w
        self.slaves = []
        self.masters = []

    def add_slave(self, slave, addr, length):
        assert isinstance(slave, AxiLiteSlave)
        self.slaves.append((slave, addr, length))

    def add_master(self, master):
        assert isinstance(master, AxiLiteMaster)
        self.masters.append(master)

    def get_instance_ports(self):
        def get_ports(interface, prefix):
            if isinstance(interface, AxiLiteMaster):
                new_type = AxiLiteSlave
            else:
                new_type = AxiLiteMaster
            new_interface = new_type(self.data_w, self.addr_w, fields=interface.fields)
            return get_ports_for_instance(new_interface, prefix=prefix)

        ports = [get_ports(slave, prefix='M_AXI_') for slave, a, l in self.slaves]
        slave_ports = {k: Cat([s[k] for s in ports]) for k in ports[0].keys()}

        ports = [get_ports(master, prefix='S_AXI_') for master in self.masters]
        master_ports = {k: Cat([s[k] for s in ports]) for k in ports[0].keys()}
        return {**slave_ports, **master_ports}

    def cat_addresses(self, addresses):
        fmt = '{{:0{}b}}'.format(self.addr_w)
        return int(''.join([fmt.format(a) for a in addresses[::-1]]), 2)

    def elaborate(self, platform):
        m = Module()

        ns = len(self.slaves)
        nm = len(self.masters)

        addresses = [a for s, a, l in self.slaves]
        masks = [length_to_mask(l, self.addr_w) for s, a, l in self.slaves]

        m.submodules.axilxbar_i = Instance(
            'axilxbar',
            p_C_AXI_DATA_WIDTH = self.data_w,
            p_C_AXI_ADDR_WIDTH = self.addr_w,
            p_NM = nm,
            p_NS = ns,
            p_SLAVE_ADDR = Const(self.cat_addresses(addresses), ns * self.addr_w),
            p_SLAVE_MASK = Const(self.cat_addresses(masks), ns * self.addr_w),
            p_OPT_LOWPOWER = 1,
            p_OPT_LINGER = 4,
            p_LGMAXBURST = 5,
            i_S_AXI_ACLK = ClockSignal(self.domain),
            i_S_AXI_ARESETN = ~ResetSignal(self.domain),
            **self.get_instance_ports(),
        )

        if isinstance(platform, Platform):
            for d in self.DEPENDENCIES:
                add_verilog_file(platform, d)

        return m

if __name__ == '__main__':
    from nmigen.cli import main

    xbar = AxiLiteXBar(32, 16)
    slave1 = AxiLiteSlave(32, 16, name='slave1')
    slave2 = AxiLiteSlave(32, 16, name='slave2')
    master1 = AxiLiteMaster(32, 16, name='master1')
    master2 = AxiLiteMaster(32, 16, name='master2')
    xbar.add_slave(slave1, 0x8000, 0x1000)
    xbar.add_slave(slave2, 0x9000, 0x1000)
    xbar.add_master(master1)
    xbar.add_master(master2)

    ports = [v for v in slave1.fields.values()]
    ports += [v for v in slave2.fields.values()]
    ports += [v for v in master1.fields.values()]
    ports += [v for v in master2.fields.values()]
    main(xbar, None, ports=ports)


