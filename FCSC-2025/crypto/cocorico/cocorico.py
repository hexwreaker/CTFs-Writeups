import os
import json
from zlib import crc32 as le_mac
from Crypto.Cipher import AES

class CocoRiCo_Chiffrement_AEAD:
	def __init__(self, la_clef):
		self.la_clef = la_clef

	def le_chiffrement(self):
		return AES.new(self.la_clef, AES.MODE_OFB, iv = b"\x00" * 16)

	def chiffrer_integre(self, le_message):
		le_tag = int.to_bytes(le_mac(le_message), 4)
		print(f"chiffrement  : {le_message + le_tag}")
		print(f"hexadecimal  : {(le_message + le_tag).hex()}")
		print(f"avec la clef : {self.la_clef.hex()}")
		return self.le_chiffrement().encrypt(le_message + le_tag)

	def dechiffrer(self, le_chiffre):
		x = self.le_chiffrement().decrypt(le_chiffre)
		le_message, t = x[:-4], x[-4:]
		le_tag = int.to_bytes(le_mac(le_message), 4)
		print(f"dechiffrement  	: {le_chiffre.hex()}")
		print(f"clair		  	: {le_message}")
		print(f"tag recv 		: {t}")
		print(f"tag calc		: {le_tag}")
		if le_tag == t:
			return le_message
		else:
			return b""

try:
	la_clef = os.urandom(32)
	E = CocoRiCo_Chiffrement_AEAD(la_clef)

	for _ in "FCSC"*100:

		print("0. Quit")
		print("1. Login")
		print("2. Logout")
		print("3. TODO")
		choice = int(input(">>> "))

		if choice == 0:
			break

		elif choice == 1:

			new = input("Are you new ? (y/n) ")
			if new == "y":

				name = input("Name: ")
				if name == "toto":
					print("Toto is one of our admin! Do not try to outsmart the system!")
					# exit(1)

				d = json.dumps({
					"name": name,
					"admin": False,
				}).encode()

				c = E.chiffrer_integre(d)
				print(f"Welcome {name}. Here is your token:")
				print(c.hex())

				logged = 1

				print("This challenge is still under active developement, please come back in a few weeks to try it out!")
				# TODO: Add vulnerable code here

			elif new == "n":

				token = bytes.fromhex(input("Token: "))
				print(f"token input : {token.hex()}")
				x = E.dechiffrer(token)
				print(f"decrypted : {x}")
				d = json.loads(x)
				if d["name"] == "toto" and d["admin"]:
					print("Congrats! Here is your flag:")
					print(open("flag.txt").read().strip())
				else:
					print(f"Weclome back {d['name']}!")

		elif choice == 2:
			logged = 0

		elif choice == 3:
			print("This challenge is still under active developement, please come back in a few weeks to try it out!")
			# TODO: Add another vuln here

except:
	print("Please check your inputs.")
