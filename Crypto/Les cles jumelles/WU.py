#!/usr/bin/env python3

"""
Étape	
1	Lecture des paramètres	lignes 5-9 solve
2	p = gcd(n1, n2)	ligne 12
3-4	Calcul de q1, φ, puis d	lignes 16-19
5	Calcul de m et conversion en bytes	lignes 22-24
"""

import math
from Crypto.Util.number import inverse
from pathlib import Path

# 1) Lecture des paramètres
n1 = int(Path("n1.txt").read_text(), 16)
n2 = int(Path("n2.txt").read_text(), 16)
e  = int(Path("e.txt").read_text())
c  = int(Path("ciphertext.txt").read_text(), 16)

# 2) Extraction du premier facteur commun p
p = math.gcd(n1, n2)
if p == 1:
    raise ValueError("Pas de prime partagée entre n1 et n2.")

# 3) Reconstruction de q1 et calcul de phi(n1)
q1 = n1 // p
phi1 = (p - 1) * (q1 - 1)

# 4) Calcul de l’exposant privé d1
d1 = inverse(e, phi1)

# 5) Déchiffrement du flag
m = pow(c, d1, n1)
flag = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")

print("🏅 Flag déchiffré :", flag.decode())
