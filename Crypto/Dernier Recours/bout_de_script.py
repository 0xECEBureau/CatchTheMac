def xor_encrypt(message, key):
    return bytes([b ^ key for b in message.encode()]).hex()

# Message secret
secret_message = "FALSE{Test}"

# Clé secrète inconnue, un entier entre 1 et 255
key = ???

# Chiffrement du message
ciphertext = xor_encrypt(secret_message, key)