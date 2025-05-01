## Principe de dissimulation (LSB Steganography)

1. **Audio PCM 16 bits**  
   - Chaque échantillon est codé sur 16 bits (2 octets).  
   - Les bits de poids faible (LSB) sont inaudibles à l’oreille lorsqu’ils changent.  

2. **Encodage du flag**  
   - Le flag ASCII (`MAC{L3_D0UX_S0N_D3_M4_V01X}`) est transformé en suite de bits (8 bits par caractère).  
   - Chaque bit du flag est injecté dans le LSB d’un échantillon audio, séquentiellement.  
   - Le reste des échantillons est laissé inchangé ou rempli de 0 (padding).

```python

#!/usr/bin/env python3
import wave

# 1. Ouvrir le WAV
wav = wave.open('discours_mac2.wav', 'rb')

# 2. Lire les frames
frames = wav.readframes(wav.getnframes())

# 3. Convertir en échantillons signés 16 bits
samples = [
    int.from_bytes(frames[i:i+2], 'little', signed=True)
    for i in range(0, len(frames), 2)
]

# 4. Extraire LSBs
bits = ''.join(str(s & 1) for s in samples)

# 5. Regrouper en octets ASCII
chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
message = ''.join(chars)

# 6. Nettoyer le padding
flag = message.split('\\x00', 1)[0]
print('Flag trouvé :', flag)
```
