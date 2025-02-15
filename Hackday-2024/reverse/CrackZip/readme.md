



# Crack a zip file

## Informations 

Fichiers :
    - SuperUltraTech30001.zip // zip chiffré
    - DS.jpeg // image de DS



> SuperUltraTech30001.zip

```sh
└─$ 7z l -slt SuperUltraTech30001.zip

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=C.UTF-8,Utf16=on,HugeFiles=on,64 bits,16 CPUs AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx   (810F81),ASM,AES-NI)

Scanning the drive for archives:
1 file, 53913 bytes (53 KiB)

Listing archive: SuperUltraTech30001.zip

--
Path = SuperUltraTech30001.zip
Type = zip
Physical Size = 53913

----------
Path = tool_retriever.py
Folder = -
Size = 1779
Packed Size = 946
Modified = 2024-01-11 02:33:07
Created = 
Accessed = 
Attributes = _ -rw-r--r--
Encrypted = +
Comment = 
CRC = A095F5D3
Method = ZipCrypto Deflate
Host OS = Unix
Version = 20
Volume Index = 0

Path = DS.jpeg
Folder = -
Size = 54019
Packed Size = 52609
Modified = 2023-12-11 13:55:42
Created = 
Accessed = 
Attributes = _ -rw-r--r--
Encrypted = +
Comment = 
CRC = 075BD07C
Method = ZipCrypto Deflate
Host OS = Unix
Version = 20
Volume Index = 0

```




## bkcrack

> https://github.com/kimci86/bkcrack




## pkcrack


> https://github.com/keyunluo/pkcrack#usage


Utilisation de la commande :

    $ pkcrack -C encrypted-ZIP -c ciphertextname -P plaintext-ZIP -p plaintextname -d decrypted_file -a

Avec :

    - encrypted-ZIP     ->  SuperUltraTech30001.zip // zip chiffré 
    - ciphertextname    ->  DS.jpeg                 // nom du fichier vulnérable
    - plaintext-ZIP     ->  DS.zip                  // zip en clair contenant le fichier vulnérable
    - plaintextname     ->  DS.jpeg                 // nom du fichier vulnérable
    - decrypted_file    ->  decrypted.zip           // nom de l'archive qui sera créée afin de stocker le contenu déchiffré


Exemple :

```
─$ pkcrack -C SuperUltraTech30001.zip -c DS.jpeg -P DS.zip -p DS.jpeg -d decrypted.zip -a
Files read. Starting stage 1 on Wed Jan 17 18:57:01 2024
Generating 1st generation of possible key2_52608 values...done.
Found 4194304 possible key2-values.
Now we're trying to reduce these...
Lowest number: 973 values at offset 47519
Lowest number: 953 values at offset 47518
...
Lowest number: 99 values at offset 47233
Done. Left with 99 possible Values. bestOffset is 47233.
Stage 1 completed. Starting stage 2 on Wed Jan 17 18:57:19 2024
Ta-daaaaa! key0=3ea43676, key1=82bd21a5, key2=3f21d103
Probabilistic test succeeded for 5380 bytes.
Ta-daaaaa! key0=3ea43676, key1=82bd21a5, key2=3f21d103
Probabilistic test succeeded for 5380 bytes.
Ta-daaaaa! key0=3ea43676, key1=82bd21a5, key2=3f21d103
Probabilistic test succeeded for 5380 bytes.
Stage 2 completed. Starting zipdecrypt on Wed Jan 17 18:57:20 2024
Decrypting tool_retriever.py (0ebce0f2969b8306b5982414)... OK!
Decrypting DS.jpeg (6690a5ac12545c7c84b9f56e)... OK!
Finished on Wed Jan 17 18:57:20 2024
```
