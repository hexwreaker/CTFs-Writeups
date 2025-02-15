from lief import *
from capstone import *
from capstone.x86 import *

md = Cs(CS_ARCH_X86, CS_MODE_64)

elf = parse("intronisation")
text_seg = elf.get_section(".text")

data = text_seg.content[0x62:0x112]

res = bytearray(16)

i = 0
for inst in md.disasm(data, 0x0):
    # print(inst)
    
    if inst.mnemonic == "add":
    
        op2 = inst.op_str.split(',')[1]
        i = int(op2, 16)
        print(str(i), end='')

    if inst.mnemonic == "cmp":
        op2 = inst.op_str.split(',')[1]
        print(chr(int(op2, 16)))
        
        res[i] = int(op2, 16)

print(str(res))
