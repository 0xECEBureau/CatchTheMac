import random
import string

def caesar_encrypt(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            encrypted += char
    return encrypted

# Message secret
secret_message = "MAC{CA3S4R_1S_3AS7}"

# Génération d'un décalage aléatoire entre 1 et 25
shift = random.randint(1, 25)

# Chiffrement du message
ciphertext = caesar_encrypt(secret_message, shift)

# Sauvegarde dans un fichier
with open("encrypted.txt", "w") as f:
    f.write(ciphertext)

print(f"Challenge généré ! Décalage secret : {shift}")  # À cacher


def caesar_decrypt(text, shift):
    decrypted = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            decrypted += char
    return decrypted

with open("encrypted.txt", "r") as f:
    ciphertext = f.read().strip()

# Brute-force sur tous les décalages possibles
for shift in range(26):
    decrypted = caesar_decrypt(ciphertext, shift)
    if "CTF{" in decrypted:
        print(f"Décalage trouvé : {shift}")
        print(f"Message déchiffré : {decrypted}")
        break
