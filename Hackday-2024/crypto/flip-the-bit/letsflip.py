from datetime import datetime, timedelta


def split(plain,ciphered,IVgive):
	clearBlock,cipherBlock = [],[]
	plain = (blocksize//4)*"_IV_" + plain if(IVgive == True) else plain
	plain = padRDN(plain)
	for i in range((len(plain)//(blocksize))):
		clearBlock.append(plain[i*blocksize:blocksize*(i+1)])
		cipherBlock.append(ciphered[(i*blocksize)*2:(blocksize*(i+1))*2])

	return clearBlock,cipherBlock

def padRDN(str_):
	while (len(str_)%blocksize != 0):
		str_+="_"
	return str_

def get_bitflip(currentBit , Letter_Spotted , Letter_edited):
	result = int(currentBit,16) ^ ord(Letter_Spotted) ^ ord(Letter_edited)
	return chr(result).encode('latin1').hex()



def flipBlock(indexBlock,indexLetter,newletter):
	indexChar = indexLetter%blocksize

	hex_spotted = CiBlock[indexBlock-1][indexChar*2:(indexChar*2)+2]
	letter_spotted = Clblock[indexBlock][indexChar:indexChar+1]

	flipped = get_bitflip(hex_spotted ,letter_spotted, newletter)

	CiBlock[indexBlock-1] = CiBlock[indexBlock-1][:indexChar*2]  + flipped + CiBlock[indexBlock-1][(indexChar*2)+2:]
	Clblock[indexBlock] =  Clblock[indexBlock][:indexChar]  + newletter + Clblock[indexBlock][(indexChar)+1:]


blocksize = 16

cleartext = "username=bdmin&agent=agence&profession=AAAAAAAA&admin=false&time=1705850224.795957"
token = "37f78ac82cf4c2a8943e8f5d61b5fd3b3f4e406d8ff84f5e6fd1c91db7b7a2f3f5c7b366e18818b99141b05fd4092624bf260ca29cd8fa4eb208a6fcac7ad0c32054d8ac1e1f3991dfb36099aab2a56b25694eeaf4fb96c10de97d6a9440b296b92f17880fd189dc59297ad38c4f72b9"

print(cleartext)
Clblock , CiBlock = split(cleartext,token,True)

print(Clblock)
print(CiBlock)

flipBlock(4,6,"t")
flipBlock(4,7,"r")
flipBlock(4,8,"u")
flipBlock(4,9,"e")
flipBlock(4,10,"&")
flipBlock(4,11,"t")

#flipBlock(1,9,"a")
#flipBlock(6,6,"t")
#flipBlock(6,7,"r")
#flipBlock(6,8,"u")
#flipBlock(6,9,"e")
#flipBlock(6,10,"&")
#flipBlock(6,11,"t")
print('\n\n')

print(Clblock)
print(CiBlock)


Final_Token = ''.join(CiBlock)

print(f'\n\nCrafted : {Final_Token}')
