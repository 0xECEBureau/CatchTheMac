import random

def xor_encrypt(message, key):
    return bytes([b ^ key for b in message.encode()]).hex()

# Message secret
secret_message = "CTF{XOR_is_fun}"

# Génération d'une clé aléatoire entre 1 et 255
key = random.randint(1, 255)
print("key used :", key)

# Chiffrement du message
ciphertext = xor_encrypt(secret_message, key)

# Sauvegarde dans un fichier
with open("ciphertext.txt", "w") as f:
    f.write(ciphertext)

print("Fichier ciphertext.txt généré.")


def xor_decrypt(ciphertext, key):
    return "".join(chr(b ^ key) for b in bytes.fromhex(ciphertext))

with open("ciphertext.txt", "r") as f:
    ciphertext = f.read().strip()

# Brute-force sur toutes les clés possibles
for key in range(256):
    decrypted = xor_decrypt(ciphertext, key)
    if "CTF{" in decrypted:  # Vérifie si le flag est lisible
        print(f"Clé trouvée : {key}")
        print(f"Message déchiffré : {decrypted}")
        break
