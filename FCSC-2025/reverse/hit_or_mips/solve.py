

import sys

def add_256bit_with_carry(temp_buff, unk_554):
    res_buff = []
    for i in range(8):
        a = (temp_buff[i*4]<<24) + (temp_buff[i*4+1]<<16) + (temp_buff[i*4+2]<<8) + temp_buff[i*4+3]
        b = unk_554[i]
        result = a + b
        print(result)
        result += (result > 0xFFFFFFFF)
        print(result)
        res_buff.append(result & 0xFFFFFFFF)  # keep it 32-bit
    return res_buff

def sub_256bit_with_borrow(res_buff, unk_554):
    temp_buff = []
    for i in range(8):
        a = res_buff[i]
        c = unk_554[i]
        # Check if result has the extra carry added
        if a - c < 0:
            b = 0xffffffff - c + a
        else:
            b = a - c
        temp_buff.append(b)

    return temp_buff

def main():
    res = 1
    temp_buff = [0] * 32
    tmp_val = [''] * 2
    input_buff = [''] * 64
    unk_533 = [125, 44, 180, 230, 166, 83, 92, 126, 97, 244, 210, 201, 76, 107, 17, 165, 63, 145, 173, 180, 187, 216, 28, 116, 25, 248, 227, 153, 129, 231, 10, 221]
    unk_554 = [0x14BC2D8A, 0xA9535C19, 0x970D4BC7, 0xDC9277A6, 0x3067A42E, 0x224E7C1E, 0x760E8367, 0xE781FA45]
    unk_574 = [0x46435343, 0x7B357538, 0x6D31375F, 0x37683135, 0x2D346E64, 0x7E313030, 0x35333D68, 0x3472647D]

    # Read input
    print("Input? ")
    # input_data = sys.stdin.read(5)
    input_data = "FCSC{"
    if input_data == "FCSC{":
        # input_buff = list(sys.stdin.read(64))
        input_buff = "7f954a7c5479dc2687b29e6d83d99f80f7c7f516ac2e5cf12d060639f80de594"
        input_buff = "ababababababababababababababababefefefefefefefefefefefefefefefef"
        print(f"input : {''.join(input_buff)}")
        r = 0
        i = 0
        while True:
            ch = input_buff[r + 62]
            tmp_val[0] = input_buff[r + 63]
            tmp_val[1] = ch  # Inverse two chars
            print(f"tmp_val : {tmp_val}; ", end='')
            try:
                intval = int(''.join(tmp_val), 16)
            except ValueError:
                intval = 0
                break
            print(f"intval : {intval}")

            temp_buff[i] = intval
            i += 1
            r -= 2
            if r == -64:
                print(f"start processing")
                res = 1
                # if sys.stdin.read(1) == '}':
                if '}' == '}':
                    print(f"temp_buff : {temp_buff}")
                    print(f"unk_533 : {unk_533}")
                    for v9 in range(32):
                        temp_buff[v9] ^= unk_533[v9]
                    print(f"xored temp_buff : {bytearray(temp_buff).hex()}")

                    temp_buff_2 = add_256bit_with_carry(temp_buff, unk_554)

                    v16 = 0
                    temp_buff_1 = 0
                    while v16 <= 8:
                    # while v16 <= 8 and temp_buff_2[v16] == unk_574[v16 ^ 7]:
                        print(f"temp_buff_2[{v16}] ({hex(temp_buff_2[v16])}) \t should be {hex(unk_574[v16 ^ 7])}")
                        v16 += 1
                        temp_buff_1 += 4
                        if v16 == 8:
                            print("Success!")
                            return 0
                    return 2
                return res
    return res

# Example usage
# if __name__ == "__main__":
#     exit(main())

def int_list_to_bytearray(int_list):
    result = bytearray()
    for val in int_list:
        result.extend(val.to_bytes(4, byteorder='big'))
    return result

def reverse_main(temp_buff_2_result):
    unk_533 = [125, 44, 180, 230, 166, 83, 92, 126, 97, 244, 210, 201, 76, 107, 17, 165, 63, 145, 173, 180, 187, 216, 28, 116, 25, 248, 227, 153, 129, 231, 10, 221]
    unk_554 = [0x14BC2D8A, 0xA9535C19, 0x970D4BC7, 0xDC9277A6, 0x3067A42E, 0x224E7C1E, 0x760E8367, 0xE781FA45]

    # Step 1: Reverse the addition operation
    temp_buff = [0] * 32
    print(temp_buff_2_result)
    temp_buff = sub_256bit_with_borrow(temp_buff_2_result, unk_554)
    print(temp_buff)
    temp_buff = int_list_to_bytearray(temp_buff)
    print(temp_buff.hex())

    # Step 2: Reverse the XOR operation
    for v9 in range(32):
        temp_buff[v9] ^= unk_533[v9]
    print(temp_buff.hex())

    # Step 3: Reconstruct the input_buff from temp_buff
    input_buff = [''] * 64
    i = 0
    for r in range(0, 64, 2):
        intval = temp_buff[i]
        tmp_val = f"{intval:02x}"[-2:]  # Convert to hex and take last two characters
        print(tmp_val)
        input_buff[63-r] = tmp_val[0]
        input_buff[62-r] = tmp_val[1]
        i += 1

    return ''.join(input_buff)

# should be :
should_be = [0x3472647d, 0x35333d68, 0x7e313030, 0x2d346e64, 0x37683135, 0x6d31375f, 0x7b357538, 0x46435343]
# abef_res = [0x988e77a2, 0x200fe9a, 0x361777ff, 0x8f286702, 0xb592bb3c, 0x23b122ec, 0x1950dc8b, 0x22dfaaad]
res = reverse_main(should_be)
print("should be : ")
print("FCSC{"+res+"}")

# FCSC{ababababababababababababababababefefefefefefefefefefefefefefefef}




