

datas = {
    'token':        "username=bdmin&agent=agence&profession=AAAAAAAAAAAAAAAAAAAAAAAA&admin=false&time=1705788478.568388",
    'token_fin':    "username=admin&agent=agence&profession=AAAAAAAAAAAAAAAAAAAAAAAA&admin=true&ttime=1705788478.568388",
    'token_enc':    "38b338acd6aa0695e0fb84d344e4148bba62d8733d04cf96fd64eb854e29f69f8f7a68be9df44cf42582a14096e15b237703c8160e16cbaf8a420bccc2b5646ee2ac062023b34fd0fa3d842c7006c557ded4e805e949651a4f544ed4951283848cc602eb1fa166f8752b6ead621901a121025ed744b3f91969229f452c81470d"
}


specs = {
    'name': 'AES CBC',
    'block_size': 16,
    'IV': [0, 0, 0, 0, 0, 0, 0, 0] # Vecteur d'initialisation
}


# D         -> plain byte
# Dfinal    -> the byte wanted
# Ep        -> encrypted preceded byte 
# 
# ret       -> the Ep byte changed
def flip_byte(D, Dfinal, Ep):


    dec = D ^ Ep

    print("D={0} , Dfinal={1} , Ep={2} , dec={3} , res={4}".format(D, Dfinal, Ep, dec, f'{(dec ^ Dfinal):0>2x}'))

    return f'{(dec ^ Dfinal):0>2x}'

def flipToken(token, token_enc, token_final):
    
    token = padToken(token, len(token_enc)/2)
    token_final = padToken(token_final, len(token_enc)/2)

    print(token)
    print(token_final)

    blocks_tok = DivToken(token)
    blocks_enc = DivTokenEnc(token_enc)
    blocks_fin = DivToken(token_final)

    print(blocks_tok)
    print(blocks_fin)
    print("bla")
    print(blocks_enc)

    token_encfinal = []
    token_encfinal.append(blocks_enc[0])


    if len(blocks_tok) != len(blocks_fin):
        return -1

    # chaque block
    for b in range (1, len(blocks_tok)):
        token_encfinal_block = []
        # chaque byte
        for i in range(0, len(blocks_tok[b])):
            # byte différents
            print(blocks_tok[b][i] + " == " + blocks_fin[b][i] + " ?")
            if blocks_tok[b][i] != blocks_fin[b][i]:
                print("flip the byte ! (b:" + str(b) + " , i:" + str(i) + ") Ep -> " + str(int(blocks_enc[b-1][i], 16)))
                # flip the bit
                token_encfinal[b-1][i] = flip_byte(ord(blocks_tok[b][i]), ord(blocks_fin[b][i]), int(blocks_enc[b-1][i], 16))

            # copy
            token_encfinal_block.append(blocks_enc[b][i])
        token_encfinal.append(token_encfinal_block)

    res = ""
    for i in range(len(token_encfinal)):
        for j in range(len(token_encfinal[i])):
            res = res + str(token_encfinal[i][j])

    return res

# padding
def padToken(token, expected_size):
    padd = "." * int(expected_size - len(token))

    return token + padd

def DivToken(token):
    blocks = []
    size = len(token)

    for b in range(size // specs['block_size']):
        blocks.append(token[b*specs['block_size']: (b+1)*specs['block_size']])

    if size % specs['block_size'] != 0:
        blocks.append(token[(size // specs['block_size'])*specs['block_size']: (size // specs['block_size'])*specs['block_size'] + size % specs['block_size']])

    return blocks

def DivTokenEnc(token_enc):
    blocks = []
    size = len(token_enc)

    for b in range(size // (specs['block_size']*2)):
        blocks.append(token_enc[b*(specs['block_size']*2): (b+1)*(specs['block_size']*2)])

    if size % (specs['block_size']*2) != 0:
        blocks.append(token_enc[(size // (specs['block_size']*2))*(specs['block_size']*2): (size // (specs['block_size']*2))*(specs['block_size']*2) + size % (specs['block_size']*2)])

    res_block = []
    for i in range(len(blocks)):
        res_b_b = []
        for j in range(int(len(blocks[i]) / 2)):
            res_b_b.append(blocks[i][j*2:(j+1)*2])
        res_block.append(res_b_b)

    return res_block


if __name__ == '__main__':

    res = flipToken(datas['token'], datas['token_enc'], datas['token_fin'])

    print(datas['token_enc'])
    print(res)

    


