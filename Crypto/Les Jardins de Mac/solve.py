#!/usr/bin/env python3
"""
Solve the "Jardin Secret" challenge using only:
- alphabet.txt (cipher alphabet for A–Z then a–z)
- jardin_secret.key2.bin (single-byte XOR key)
- jardin_secret.xml.enc (double-encrypted XML)

Steps:
1) Read XOR key and reverse XOR
2) Build inverse substitution map from alphabet.txt
3) Apply inverse substitution to reveal XML
4) Extract and print flag
"""
import re
from pathlib import Path

# --- Step 1: Reverse XOR encryption ---
enc_data = Path("jardin_secret.xml.enc").read_bytes()
xor_key = Path("jardin_secret.bin").read_bytes()[0]
data_xor = bytes(b ^ xor_key for b in enc_data)

# --- Step 2: Build inverse substitution map from alphabet.txt ---
# alphabet.txt: 52 chars, first for A-Z, next for a-z
cipher_seq = Path("alphabet.txt").read_text().strip()
plain_seq = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
sub_map = {cipher_seq[i]: plain_seq[i] for i in range(len(plain_seq))}
inv_map = {ord(c): ord(p) for c, p in sub_map.items()}

# --- Step 3: Apply inverse substitution ---
decoded = bytearray()
for b in data_xor:
    decoded.append(inv_map.get(b, b))

# Write out decrypted XML
out_path = "jardin_secret_decrypted.xml"
Path(out_path).write_bytes(decoded)
print(f"Decrypted XML written to {out_path}")

# --- Step 4: Extract flag ---
m = re.search(rb"<flag>(MAC\{[^<]+\})</flag>", decoded)
if m:
    print("Flag:", m.group(1).decode())
else:
    print("Flag not found in decrypted XML.")
