# Write-up : 03 - Le Masque Trompeur

## Objectif
Ce challenge vise à tester la compréhension du fonctionnement des sous-réseaux IP.

Le joueur est confronté à un fichier de logs contenant des pings et des résolutions ARP réussies ou échouées. L'objectif est de comprendre que certains échecs s'expliquent par un **masque de sous-réseau plus restrictif** que celui affiché.

---

## Analyse pas à pas

1. **Observation de la configuration réseau dans les logs**
   ```
   ifconfig eth0
   inet addr:192.168.2.10  Bcast:192.168.2.255  Mask:255.255.255.0
   ```
   ✅ On pense être dans un /24 (192.168.2.0 à 192.168.2.255)

2. **Analyse des pings**
   ```
   ping 192.168.2.1 - SUCCESS
   ping 192.168.2.30 - SUCCESS
   ping 192.168.2.31 - NO REPLY
   ping 192.168.2.32 - Destination Host Unreachable
   ```
   ✅ Tout ce qui est **au-dessus de .30** échoue.

3. **Vérification par calcul de sous-réseau**
   Si le masque réel était `255.255.255.224` (soit /27), alors :
   - Plage IP : 192.168.2.1 → 192.168.2.30
   - Broadcast : 192.168.2.31
   ✅ Donc 192.168.2.31 est le broadcast, 192.168.2.32 est **hors-réseau**.

4. **ARP confirmant les limites**
   ```
   arping 192.168.2.30 - response from 00:11:22:33:44:1E
   arping 192.168.2.31 - NO RESPONSE
   ```
   ✅ Même comportement : seul .30 est atteignable.

5. **Conclusion**
   Le masque réel n'est **pas /24**, mais bien **/27**, soit :
   ```
   255.255.255.224
   ```

---

## Flag
```
MAC{255.255.255.224}
```
