from sympy import mod_inverse
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# Given remainders from the output
remainders = {
    "carotte": 392278890668246705,
    "radis": 4588810924820033807,
    "tomate": 17164682861166542664,
    "pomme": 12928514648456294931,
    "banane": 5973470563196845286
}

# Given moduli
moduli = {
    "carotte": 17488856370348678479,
    "radis": 16548497022403653709,
    "tomate": 17646308379662286151,
    "pomme": 14933475126425703583,
    "banane": 17256641469715966189
}

def find_key_crt_corrected(remainders, moduli):
    M = 1
    for m in moduli.values():
        M *= m
    
    Mi = {mod: M // mod for mod in moduli.values()}
    print(Mi)
    yi = {mod: mod_inverse(Mi[mod], mod) for mod in moduli.values()}
    
    x = sum(remainders[var] * Mi[moduli[var]] * yi[moduli[var]] for var in remainders)
    
    return x % M

# Find the key with corrected function
key_int = find_key_crt_corrected(remainders, moduli)
key_bytes = key_int.to_bytes(32, byteorder='big')
print(key_bytes)


# The key retrieved using CRT
key_bytes = b'\x81k9%8\xaeX\x95\t>\n\x80\x94\xa2\xb8X\xa1\xc2\xbd\xc1e\x87\xeb\xfb\xd8\x0f\xd5\x0f~\x19 M'

# The encrypted data (hex encoded)
encrypted_data_hex = "2da1dbe8c3a739d9c4a0dc29a27377fe8abc1c0feacc9475019c5954bbbf74dcedce7ed3dc3ba34fa14a9181d4d7ec0133ca96012b0a9f4aa93c42c61acbeae7640dd101a6d2db9ad4f3b8ccfe285e0d"
encrypted_data = bytes.fromhex(encrypted_data_hex)

# Create a cipher object using the key and encrypted data
cipher = AES.new(key_bytes, AES.MODE_ECB)

# Decrypt the data
decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

# Print the decrypted data
print("Decrypted data:", decrypted_data.decode('utf-8'))