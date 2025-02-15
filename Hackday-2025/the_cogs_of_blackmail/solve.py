import dnfile
import pefile
from Crypto.Cipher import AES

DLL = "DLLinner_"

def get_text_section_pointer_to_raw_data(DLL_filename):
    pe = pefile.PE(DLL_filename)
    for section in pe.sections:
        if section.Name.decode('utf-8').strip('\x00') == '.text':
            print(section.PointerToRawData)
            return section.PointerToRawData
    return None

def get_rva(DLL_filename, field_id):
    # Load the PE file
    pe = dnfile.dnPE(DLL_filename)
    # Access the metadata tables
    md_tables = pe.net.mdtables

    # Iterate over the FieldRVA table entries
    for field_rva in md_tables.FieldRva.rows:
        if field_rva.struct.Field_Index == field_id:
            return field_rva.struct.Rva

def decrypt():
    key = open("key", 'rb').read()
    iv = open("iv", 'rb').read()
    encs = open("encs", 'rb').read()
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    decs = decryptor.decrypt(encs)
    i = open("DLL.dll", 'wb').write(decs)

def parse_key(DLL_filename, dll_bytes):
    # 1F 20 8D 19 00 00 01 25 D0 xx
    # xx = place dans le mdtable
    loc = dll_bytes.find(bytes.fromhex("1F208D1900000125D0"))
    xx = dll_bytes[loc+9]
    print(xx)
    rva = get_rva(DLL_filename, xx)
    print(rva)
    key_addr = get_text_section_pointer_to_raw_data(DLL_filename) + rva - 0x2000
    return dll_bytes[key_addr:key_addr+32]

def parse_iv(DLL_filename, dll_bytes):
    # 1F 10 8D 19 00 00 01 25 D0 xx
    # xx = place dans le mdtable
    loc = dll_bytes.find(bytes.fromhex("1F108D1900000125D0"))
    xx = dll_bytes[loc+9]
    rva = get_rva(DLL_filename, xx)
    iv_addr = get_text_section_pointer_to_raw_data(DLL_filename) + rva - 0x2000
    return dll_bytes[iv_addr:iv_addr+16]

def parse_encs(DLL_filename, dll_bytes):
    # 1F 10 8D 19 00 00 01 25 D0 xx
    # xx = place dans le mdtable
    loc = 0
    while (True):
        loc = dll_bytes.find(bytes.fromhex("8D1900000125D0"), loc+1)
        if dll_bytes[loc-5] == 0x20:
            loc -= 4
            break
    
    size = int.from_bytes(dll_bytes[loc:loc+4], 'little')
    xx = dll_bytes[loc+11]
    rva = get_rva(DLL_filename, xx)
    iv_addr = get_text_section_pointer_to_raw_data(DLL_filename) + rva - 0x2000
    return dll_bytes[iv_addr:iv_addr+size]

def main():
    i = 60
    while True:
        dll_filename = "DLL_"+str(i)+".dll"
        out_dll_filename = "DLL_"+str(i+1)+".dll"
        print(f"\"{dll_filename}\" extracting to \"{out_dll_filename}\"...")

        dll = open(dll_filename, "rb").read()

        key = parse_key(dll_filename, dll)
        iv = parse_iv(dll_filename, dll)
        encs = parse_encs(dll_filename, dll)
        print(f"\tkey: {key.hex()}")
        print(f"\tiv : {iv.hex()}")
        print(f"\twrite : {len(encs)}")

        decryptor = AES.new(key, AES.MODE_CBC, iv)
        decs = decryptor.decrypt(encs)

        dll_out = open(out_dll_filename, 'xb').write(decs)
        if (decs[:2] == b"MZ"):
            print(f"\tdiscover a new DLL !")
        else:
            print(f"\tAAAAhh discover something that is not a DLL !!!")
            break
        i += 1

# main()
dll_filename = "DLL_149.dll"
dll = open(dll_filename, "rb").read()
key = parse_key(dll_filename, dll)
iv = parse_iv(dll_filename, dll)
encs = parse_encs(dll_filename, dll)
print(f"\tkey: {key.hex()}")
print(f"\tiv : {iv.hex()}")
print(f"\twrite : {len(encs)}")