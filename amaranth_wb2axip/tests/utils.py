import subprocess
from amaranth.build import *
from amaranth.hdl.ir import Fragment
from amaranth.build.plat import TemplatedPlatform
from amaranth.back import rtlil
from amaranth._toolchain import require_tool
import tempfile

class EmptyPlatform(Platform):
    connectors = []
    required_tools = []
    resources = []
    toolchain = 'yosys'

    def toolchain_prepare(self):
        pass

def synth(core, ports):
    plat = EmptyPlatform()
    frag = Fragment.get(core, plat)
    rtlil_text = rtlil.convert(frag, ports=ports)

    yosys_cmd = ''
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(temp_dir + '/top.il', 'w') as f:
            f.write(rtlil_text)

        for file_name, content in plat.extra_files.items():
            with open(temp_dir + '/' + file_name, 'wb') as f:
                f.write(content)
            yosys_cmd += "read_verilog {}\n".format(file_name)
        yosys_cmd += 'read_ilang {}\n'.format('top.il')
        yosys_cmd += 'synth_xilinx -top top\n'

        with open(temp_dir + '/top.ys', 'w') as f:
            f.write(yosys_cmd)

        subprocess.check_call([require_tool("yosys"), 'top.ys'], cwd=temp_dir)
