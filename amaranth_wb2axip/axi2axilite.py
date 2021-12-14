from amaranth import Elaboratable, Instance, ClockSignal, ResetSignal, Module
from amaranth.build.plat import Platform
from .interfaces import AxiSlave, AxiLiteMaster
from .utils import get_ports_for_instance, add_verilog_file


class Axi2AxiLite(Elaboratable):
    DEPENDENCIES = ['axi2axilite.v', 'skidbuffer.v', 'axi_addr.v', 'sfifo.v']

    def __init__(self, data_w, addr_w, id_w, domain='sync'):
        self.data_w = data_w
        self.addr_w = addr_w
        self.id_w = id_w
        self.domain = domain
        self.axilite = AxiLiteMaster(data_w, addr_w, name='M_AXI')
        self.axi = AxiSlave(data_w, addr_w, id_w, user_w=0, name='S_AXI')

    def elaborate(self, platform):
        m = Module()
        m.submodules.axi2axil_i = Instance(
            'axi2axilite',
            p_C_AXI_ID_WIDTH=self.id_w,
	        p_C_AXI_DATA_WIDTH=self.data_w,
	        p_C_AXI_ADDR_WIDTH=self.addr_w,
            i_S_AXI_ACLK=ClockSignal(self.domain),
            i_S_AXI_ARESETN=~ResetSignal(self.domain),
            **get_ports_for_instance(self.axi, prefix='S_AXI_'),
            **get_ports_for_instance(self.axilite, prefix='M_AXI_'),
        )
        if isinstance(platform, Platform):
            for d in self.DEPENDENCIES:
                add_verilog_file(platform, d)
        return m


if __name__ == '__main__':
    from amaranth.cli import main
    core = Axi2AxiLite(32, 8, 5)
    ports = [v for v in core.axi.fields.values()]
    ports += [v for v in core.axilite.fields.values()]
    main(core, None, ports=ports)
