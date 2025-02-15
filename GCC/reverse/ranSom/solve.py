

dec = ""
enc = b"\x24\x27\x22\x13\x33\x60\x2a\x36\x2f\x5b\x3f\x5f\x27\x24\x38\x49\x41\x14"
node = "debian"

v1 = 0
for c in enc:
    #print(ord(node[v1]) ^ (c-1), end='')
    print(chr(ord(node[v1]) ^ (c-1)), end='')
    v1 = (v1 + 1) % 6

print(dec)


#gCC{S1mPL3_0bFU!!}