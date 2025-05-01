


# Grand Classic Hotel

Il est possible de rejouer la trace RFID Mifare Classic avec proxmark3.

Ainsi, nous observons les données des 16 secteurs de la carte.

Le flag est contenu dans le deuxième secteur :

```sh
# SECTOR 0
#   block 0 : b'FCSC{dca41bafe48\x04\x8e'
DA! 06  88  FD  5B  5C  59! D0! 23! AD! 5F  D7  27  76  7C! D5! 70  F9
46  43  53  43  15  08  04  00  47  59  55  D1  41  10  36  07  8F  31
#   block 1
4C  8F  8B  E4! BD! 59! 67  AF  00  CC! 19! 16  57  CF  AA! 9E! 32
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  37  49
#   block 2
49  C7  5F! E3  C7  5B  D5! A4  27! 3F! E5  F1  33! 81! 17  2D  8A
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  37  49
#   block 3
D0  4B! 59  DA! 42! 6B  D8! 00  3F  CA! D0! F1  80! EB! F4  C6! 7B! 34
00  00  00  00  00  00  FF  07  80  69  FF  FF  FF  FF  FF  FF  D4  55

# SECTOR 1
#   block 4 : b'FCSC{dca41bafe48\x04\x8e'
D4! D5  AB  F2! D0  F1  D5  00! B0! 8A  42  E8  CF  19! 6A! 18  F1! 93
46  43  53  43  7B  64  63  61  34  31  62  61  66  65  34  38  04  8E
#   block 5 : b'c57bf2c9309c485d\xb6\xd3'
16! E7! 7E  D9  90  24  70  A6! E4  3C! AC! 5A! E3  F4! F8! 3C  BD! 65!
63  35  37  62  66  32  63  39  33  30  39  63  34  38  35  64  B6  D3
#   block 6 : b'a267d23de04f9}\x00\x00J\x9f'
1F! FB  C0! C2  FC! E4  32! C6! CF! D7  3E! 01  98! 25  45! B8! 73! 8A
61  32  36  37  64  32  33  64  65  30  34  66  39  7D  00  00  4A  9F
#   block 7
72! 63! A3  CC  D8  72! F0  4B  F1! 6A! F0  45! 6D! 03  91  AE! B2  9F
00  00  00  00  00  00  FF  07  80  69  FF  FF  FF  FF  FF  FF  D4  55
```


