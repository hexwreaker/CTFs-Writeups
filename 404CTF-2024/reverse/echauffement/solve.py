from lief import *


elf = parse("echauffement.bin")


# Retrieve the secret
data_section = elf.get_section(".rodata")
print(data_section.content[8:0x2a].hex())

secret = data_section.content[8:0x2a]

r = ""
for i in range(0x22):
    # print(hex(secret[i]))
    r += chr((secret[i]+i)//2)

print(r)



