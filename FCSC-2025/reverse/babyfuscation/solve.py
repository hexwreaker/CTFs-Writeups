

# get the "obfuscated" flag 
obf_flag = b'-8\xbf2\xf0\x05\xa8\xb5\x04\x9b\x8cS\xca\xe7\xf0g\xf6Y\xc4\xf1P\xe7z\xa5t\xab\xdc\xd9P\xf7Z\xbd\xb6+\x9e1\x907\x08\x1d>\xa9,i\ng8\x9f\x0e+$\x93r\x1f@m\xd4{\xeeQ\x1aO\xcam\xec\xf1$\xcbr\x05\xf1'

def reverse_process_input(processed_input):
    original_input = []
    length = len(processed_input)

    for i in range(length):
        # Undo the XOR operation
        # print(processed_input[i])
        intermediate = processed_input[i] ^ ((3 * i + 31) & 0xff)
        # reverse the OR
        #   1. the ">> 5"
        #       so we reverse with "<< 5"
        #   2. the "* 8"
        #       we know that * 8 is the same as << 3
        #       so we reverse with "<< 3"
        original_char = (intermediate >> 3) & 0xff
        original_char |= (intermediate << 5) & 0xff
        original_input.append(original_char)

    # Convert the list of characters back to a string
    return ''.join(chr(c) for c in original_input)

# Example usage
original_input = reverse_process_input(obf_flag)
print("Original Input:", original_input)
