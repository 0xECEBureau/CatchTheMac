# Write-up : 01 - La Fréquence du Mensonge

## Objectif

Ce challenge vise à illustrer la couche physique du modèle OSI. L’idée est de faire comprendre que les données, avant toute interprétation protocolaire, ne sont qu’un flux de bits transportés par des signaux physiques.

## Énoncé

Un fichier `signal.csv` est fourni. Il contient deux colonnes : `time` et `value`.
- `time` représente le temps (fictif) d'échantillonnage.
- `value` est une suite de 0 et de 1 qui simule un signal numérique binaire stable.

Chaque bit est répété 10 fois pour simuler la stabilité du signal à travers le temps. L'utilisateur doit retrouver la séquence binaire d'origine, bit par bit, en extrayant un bit toutes les 10 valeurs.

Cette séquence binaire correspond à une chaîne de caractères encodée en ASCII. Une fois la conversion effectuée, l'utilisateur obtient le flag.

## Solution pas à pas

1. **Charger le fichier CSV** dans Python
2. **Extraire la valeur d’un bit tous les 10 échantillons** 
3. **Recomposer la chaîne binaire** : chaque séquence de 8 bits représente un caractère ASCII.
4. **Convertir en texte** : utiliser un convertisseur binaire → ASCII.

### Exemple en Python
```python
import pandas as pd

# Charger le fichier
df = pd.read_csv("signal.csv")

# Récupérer 1 valeur toutes les 10 lignes (1 bit = 10 samples)
bits = df['value'][::10].tolist()

# Regrouper par 8 bits (1 octet)
binary_chars = [''.join(map(str, bits[i:i+8])) for i in range(0, len(bits), 8)]

# Convertir en texte
flag = ''.join([chr(int(b, 2)) for b in binary_chars])
print(flag)
```

## Flag
```
00:1a:cd:ef:42:00
```

Ce flag est une adresse MAC qui servira de point de départ pour identifier l’attaquant dans le challenge suivant (Couche 2).
