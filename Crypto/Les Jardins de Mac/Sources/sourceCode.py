#!/usr/bin/env python3
import json, random
from pathlib import Path

# --- Chargement du XML en clair ---
xml = Path("original.xml").read_bytes()

# --- 1) Génération de la substitution monoalphabétique ---
alphabet = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
shuffled = alphabet.copy()
random.shuffle(shuffled)
sub_map = {plain: cipher for plain, cipher in zip(alphabet, shuffled)}
# Sauvegarde de la map complète pour vérification
Path("substitution_map.json").write_text(json.dumps(sub_map, indent=2))

# --- Écriture de la colonne de droite (cipher alphabet) dans alphabet.txt ---
# Les 26 premiers caractères correspondent à A-Z, les 26 suivants à a-z
cipher_sequence = "".join(sub_map[chr(i)] for i in range(65, 91)) + "".join(sub_map[chr(i)] for i in range(97, 123))
Path("alphabet.txt").write_text(cipher_sequence)


def apply_substitution(data: bytes, mapping: dict) -> bytes:
    out = bytearray()
    for b in data:
        c = chr(b)
        out.append(ord(mapping[c]) if c in mapping else b)
    return bytes(out)

# --- 2) Chiffrement du mot “GARDEN” pour key1.txt ---
garden_enc = apply_substitution(b"GARDEN", sub_map)
Path("jardin_secret.key1.txt").write_bytes(garden_enc)

# --- 3) Chiffrement du XML par substitution ---
xml_sub = apply_substitution(xml, sub_map)

# --- 4) Génération de la clé XOR (octet) et application ---
key2 = random.randint(1, 255)
Path("jardin_secret.key2.bin").write_bytes(bytes([key2]))
xml_xor = bytes(b ^ key2 for b in xml_sub)
Path("jardin_secret.xml.enc").write_bytes(xml_xor)

# --- 5) Génération de prefix.hex pour indice ---
hex_pref = xml_xor[:20]
Path("prefix.hex").write_text(" ".join(f"{b:02x}" for b in hex_pref))

print("✅ Fichiers générés :")
print("  - substitution_map.json")
print("  - alphabet.txt (colonne de droite de la substitution)")
print("  - jardin_secret.key1.txt")
print(f"  - jardin_secret.key2.bin (clé XOR = {key2})")
print("  - jardin_secret.xml.enc")
print("  - prefix.hex")