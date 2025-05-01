


# Bigorneau


Le serveur attend une suite de caractère hexadécimaux correspondant à une shellcode x64. Le shellcode est exécuté uniquement s'il vérifie les contraintes suivantes : 

```py
assert len(SC) <= 128
assert len(set(SC)) <= 6
```

Il est important de noter que tous les registres sont mis à zero juste avant l'exécution du shellcode.

## Stratégie 1

L'objectif est d'ouvrir un shell sur la cible, donc il faut pouvoir appeler le syscall **execve**. Cepandant, les contraintes ne permettent pas de faire cet appel directement.

La première idée qui m'est venue à l'esprit est de créer un shellcode "builder" qui sert à construire un second shellcode qui lui contient l'appel à execve.

Le "builder" utiliserait les instructions ci-dessous pour construire les valeurs dans le registre RAX et les pousser sur la pile. Puis il exécute la stack.

```sh
inc eax
sal rax
push rax
jmp rsp
```

Malheureusement, je n'ai pas toruvé de combinaisons d'opcodes/opérandes qui passe la contrainte des 6 octets uniques (j'ai réussi avec 7 au minimum).


## Stratégie 2

La solution consiste à appeler le syscall **"read"** puis d'envoyer le second shellcode. Cela est possible avec le premier étage suivant : 

```sh
xor rsi, rsp
mov dl, 0xb2
syscall
```

Voir le script **solve.py**.








