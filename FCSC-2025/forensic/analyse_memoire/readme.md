

> https://hacktivity.fr/volatility-3-cheatsheet




# Analyse mémoire

Voici certaines commandes utiles pour retrouver les informations demandées.

## Get ipv4

    $ vol -f analyse-memoire.dmp windows.netstat

> **Answer :** 10.0.2.15


## Get username 

    $ vol -f analyse-memoire.dmp windows.registry.hivelist

> **Answer :** userfcsc-10

## Get machine name

    $ vol -f analyse-memoire.dmp windows.registry.printkey.PrintKey --key "ControlSet001\\Control\\ComputerName\\ComputerName"

> **Answer :** DESKTOP-JV996VQ


flag  = FCSC{userfcsc-10:DESKTOP-JV996VQ:10.0.2.15}

# 2/2

## Get doc editor name

    $ vol -f analyse-memoire.dmp windows.pslist

> **Answer :** 9048    8968    soffice.bin     0xa50a297e7240  13      -       1       False   2025-04-01 22:11:34.000000 UTC  N/A     Disabled

## Get document name 

    $ vol -f analyse-memoire.dmp windows.handles --pid 9048 | grep -i file 


> **Answer :** [SECRET-SF][TLP-RED]Plan FCSC 2026.odt

flag  = FCSC{soffice.bin:[SECRET-SF][TLP-RED]Plan FCSC 2026.odt}

## Get malware processus

> FCSC{msedge.exe:7232:185.89.208.19:443:TCP}