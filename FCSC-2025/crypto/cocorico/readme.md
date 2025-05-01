

# Cocorico

Il faut forger un chiffré pour le plaintext correspondant à : 

```py
{
    "name": "toto",
    "admin": True
}
```

Pour cela, on exploit le mode OFB d'AES en recalculant le keystream à partir d'un chiffré et de son plaintext.

Voir : **solve.py**
