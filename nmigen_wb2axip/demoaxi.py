from nmigen import Elaboratable, Instance, ClockSignal, ResetSignal, Module
from nmigen.build.plat import Platform
from .interfaces import AxiLiteSlave
from .utils import get_ports_for_instance, add_verilog_file


class DemoAxi(Elaboratable):
    DEPENDENCIES = ['demoaxi.v']

    def __init__(self, data_w, addr_w, domain='sync'):
        self.data_w = data_w
        self.addr_w = addr_w
        self.domain = domain
        self.axilite = AxiLiteSlave(data_w, addr_w, name='S_AXI')

    def elaborate(self, platform):
        m = Module()
        m.submodules.demoaxi_i = Instance(
            'demoaxi',
	        p_C_S_AXI_DATA_WIDTH=self.data_w,
	        p_C_S_AXI_ADDR_WIDTH=self.addr_w,
            i_S_AXI_ACLK=ClockSignal(self.domain),
            i_S_AXI_ARESETN=~ResetSignal(self.domain),
            **get_ports_for_instance(self.axilite, prefix='S_AXI_'),
        )

        if isinstance(platform, Platform):
            for d in self.DEPENDENCIES:
                add_verilog_file(platform, d)
        return m


if __name__ == '__main__':
    from nmigen.cli import main
    core = DemoAxi(32, 8)
    ports = [v for v in core.axilite.fields.values()]
    main(core, None, ports=ports)
