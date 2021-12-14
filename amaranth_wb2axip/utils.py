from urllib import request
from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT, Record


def dir_prefix(d):
    assert d in [DIR_FANIN, DIR_FANOUT]
    return 'i_' if d == DIR_FANIN else 'o_'


def get_ports_for_instance(rec, prefix=''):
    assert isinstance(rec, Record)
    directions = {k: d for k, (s, d) in rec.layout.fields.items()}
    return {
        dir_prefix(directions[name]) + prefix + name: signal
        for name, signal in rec.fields.items()
    }


def add_verilog_file(plat, file_name):
    URL_FMT = "https://raw.githubusercontent.com/ZipCPU/wb2axip/master/rtl/{}"
    if file_name not in plat.extra_files:
        url = URL_FMT.format(file_name)
        content = request.urlopen(url).read()
        plat.add_file(file_name, content)
