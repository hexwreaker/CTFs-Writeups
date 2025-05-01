import json
from zlib import crc32 as le_mac
from pwn import xor  # pip install pwntools
from pwn import *  # pip install pwntools

context.log_level = "debug"

# retrieve the aaaa token
io = remote("chall.fcsc.fr", 2150)
io.recvuntil(b">>> ")
io.sendline(b"1")
io.recvuntil(b'Are you new ? (y/n) ')
io.sendline(b"y")
io.recvuntil(b'Name: ')
io.sendline(b"aaaa") # aaaa is the asked name
io.recvuntil(b"Here is your token:\n")
cipher_hex = io.recv(72).decode()
cipher_bytes = bytes.fromhex(cipher_hex)

# Calc the AES OFB keystream from token and original bytes
original = {
    "name": "aaaa",
    "admin": False,
}
original_bytes = json.dumps(original).encode()
original_tag = int.to_bytes(le_mac(original_bytes), 4)
original_full = original_bytes + original_tag
keystream = xor(cipher_bytes, original_full)

print(f"original : \t{original_full.hex()}")
print(f"keystream : \t{keystream.hex()}")

# Bulid the new token
target = {
    "name": "toto",
    "admin": True
}
target_bytes = json.dumps(target).encode()
target_tag = int.to_bytes(le_mac(target_bytes), 4)
target_full = target_bytes + target_tag
print(f"target_full : \t{target_full.hex()}")

# Forge the ciphertext
forged_token = xor(target_full, keystream[:-1])
print("Use this forged token:")
print(forged_token.hex())

# Authenticate to server
io.recvuntil(b">>> ")
io.sendline(b"1")
io.recvuntil(b'Are you new ? (y/n) ')
io.sendline(b"n")
io.recvuntil(b"Token: ")
io.sendline(forged_token.hex())
io.interactive()
