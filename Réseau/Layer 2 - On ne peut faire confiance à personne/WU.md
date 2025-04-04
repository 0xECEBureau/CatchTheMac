# Write-up : Layer 2 - On ne peut faire confiance à personne

## Objectif
Ce challenge illustre la couche Liaison (2) du modèle OSI, et spécifiquement la vulnérabilité ARP qui permet d’usurper l’identité d’un hôte sur un réseau local.

## Énoncé résumé
Vous disposez d’un fichier `.pcap` contenant une série de paquets ARP (avant et après une attaque). L’adresse MAC incriminée est `00:1a:cd:ef:42:00`. Il faut retrouver l'addresse IP réelle de l’attaquant et le numéro de paquet à l’origine de l’attaque.

## Démarche pas à pas

1. **Charger le `.pcap` dans Wireshark**
   - Pour clarifier la vue, vous pouvez déjà appliquer un filtre ARP :
     ```
     arp
     ```
   - Vous verrez les requêtes et réponses ARP successives.

2. **Repérer l’attaque ARP** :
   - Vous cherchez un moment où la MAC `00:1a:cd:ef:42:00` **répond** à la place de la passerelle, par exemple :
     > "192.168.1.1 is at 00:1a:cd:ef:42:00"
   - Cela signale un ARP Spoofing : la victime (et possiblement d’autres machines) pensent que `192.168.1.1` correspond à `00:1a:cd:ef:42:00`.

3. **Filtrer sur la MAC de l’attaquant** pour isoler son trafic :
   ```
   eth.addr == 00:1a:cd:ef:42:00
   ```
   - Vous pouvez ainsi voir **TOUS** les paquets (ARP ou autre) où l’attaquant est émetteur ou destinataire.
   - En particulier, regardez les requêtes ARP émises par cette MAC.

4. **Observer la requête ARP où l’attaquant révèle son IP** :
   - Si vous voyez par exemple :
     > "Who has 192.168.1.100 ? Tell 192.168.1.13"
     et que l’emetteur (MAC `00:1a:cd:ef:42:00`) déclare `192.168.1.13` comme source IP,
     alors on comprend que **192.168.1.66** = IP réelle de l'attaquant.

## Flag

Pour répondre, fournissez simplement l’adresse IP de l’attaquant, au format IPv4. Ex :
```
MAC{192.168.1.13}
```
