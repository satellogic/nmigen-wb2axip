from amaranth import Module
from amaranth_wb2axip.demoaxi import DemoAxi
from amaranth_wb2axip.axi2axilite import Axi2AxiLite
from amaranth_wb2axip.axilxbar import AxiLiteXBar
from amaranth_wb2axip.interfaces import *
from .utils import synth


def test_synth_demo():
    demo = DemoAxi(32, 16)
    synth(demo, ports=list(core.axilite.fields.values()))


def test_synth_axi2axilite():
    axi2axil = Axi2AxiLite(32, 16, 5)
    ports = list(axi2axil.axilite.fields.values()) + list(axi2axil.axi.fields.values())
    synth(axi2axil, ports=ports)


def test_synth_axilxbar():
    xbar = AxiLiteXBar(32, 16)
    slaves = [AxiLiteSlave(32, 16) for i in range(5)]
    masters = [AxiLiteMaster(32, 16) for i in range(2)]
    for i, s in enumerate(slaves):
        xbar.add_slave(s, 0x1000 * i, 0x1000)
    for m in masters:
        xbar.add_master(m)
    ports = [field for interface in slaves + masters for field in interface.fields.values()]
    synth(xbar, ports)


def test_synth_realcase():
    m = Module()
    m.submodules.axi2axil = axi2axil = Axi2AxiLite(32, 16, 5)
    m.submodules.xbar = xbar = AxiLiteXBar(32, 16)
    slaves = [DemoAxi(32, 16) for _ in range(5)]
    for i, s in enumerate(slaves):
        m.submodules['slave_' + str(i)] = s
        xbar.add_slave(s.axilite, 0x1000 * i, 0x1000)
    xbar.add_master(axi2axil.axilite)
    ports = list(axi2axil.axi.fields.values())
    synth(m, ports)
