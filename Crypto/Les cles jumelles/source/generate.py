#!/usr/bin/env python3
import random
from Crypto.Util import number
from pathlib import Path

# 1) Génération des trois grands premiers (1024 bits chacun)
p  = number.getPrime(1024)
q1 = number.getPrime(1024)
q2 = number.getPrime(1024)
# S’assurer que q1 et q2 diffèrent de p
while q1 == p:
    q1 = number.getPrime(1024)
while q2 == p or q2 == q1:
    q2 = number.getPrime(1024)

# 2) Calcul des modules
n1 = p * q1
n2 = p * q2

# 3) Exposant public
e = 65537

# 4) Flag et chiffrement sous la première clé
flag = b"MAC{SH4R3D_PR1M3_RSA}"
m = int.from_bytes(flag, byteorder="big")
ciphertext = pow(m, e, n1)

# 5) Écriture des fichiers
Path("n1.txt").write_text(hex(n1)[2:])             # module 1 en hex
Path("n2.txt").write_text(hex(n2)[2:])             # module 2 en hex
Path("e.txt").write_text(str(e))                   # exposant
Path("ciphertext.txt").write_text(hex(ciphertext)[2:])  # ciphertext en hex

print("✅ Fichiers générés : n1.txt, n2.txt, e.txt, ciphertext.txt")
