## Principe de dissimulation (LSB Steganography)

1. **Image RGB 24 bits**  
   - Chaque pixel d'une image couleur est codé sur 24 bits (8 bits par composante R, G, B).  
   - Les bits de poids faible (LSB, Least Significant Bit) de chaque composante sont pratiquement imperceptibles à l'œil humain lorsqu'ils changent.  

2. **Encodage du flag**  
   - Le flag ASCII (`MAC{L3s_M0ust4ch3s_Du_Ch4t_C4ch3nt_D3s_B1ts}`) est transformé en une suite de bits (8 bits par caractère).  
   - Chaque bit du flag est injecté dans le LSB d'une composante de couleur d'un pixel, séquentiellement.  
   - Le reste des bits est laissé inchangé ou rempli de 0 (padding) pour marquer la fin du message.  

```python
#!/usr/bin/env python3
from PIL import Image

# 1. Ouvrir l'image
img = Image.open('Ressources/miaou.png')

# 2. Convertir en RGB si nécessaire
if img.mode != 'RGB':
    img = img.convert('RGB')

# 3. Lire les pixels
pixels = list(img.getdata())

# 4. Extraire les LSBs
bits = ''
for pixel in pixels:
    r, g, b = pixel
    bits += str(r & 1)  # Bit LSB de la composante rouge
    bits += str(g & 1)  # Bit LSB de la composante verte
    bits += str(b & 1)  # Bit LSB de la composante bleue
    if len(bits) >= 8 and bits[-8:] == '00000000':  # Délimiteur de fin
        break

# 5. Regrouper en octets ASCII
chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits) - 8, 8)]
message = ''.join(chars)

# 6. Nettoyer le padding
flag = message.split('\\x00', 1)[0]
print('Flag trouvé :', flag)

## Résolution du challenge

Pour résoudre ce challenge, suivez ces étapes :
1. Téléchargez la photo dans "Ressources/miaou.png" fournie dans le challenge.
2. Exécutez le script Python ci-dessus pour extraire le message caché.
3. Le script lira les bits LSB des composantes de couleur des pixels pour reconstruire le message binaire, puis le convertira en texte.
4. Vous obtiendrez ainsi le flag au format `MAC{flag}`.