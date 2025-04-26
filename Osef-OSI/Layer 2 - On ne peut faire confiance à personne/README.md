# Layer 2 - On ne peut faire confiance à personne

**Niveau :** moyen

Maintenant que vous avez décodé le signal intercepté, vous avez une addresse MAC. Cette identité n’apparaît dans aucune documentation officielle du réseau de 0xECE.

Un enregistrement réseau a été récupéré juste avant la disparition de Mac. Des anomalies de communication ont été détectées dans la résolution ARP du réseau local. Quelqu’un a tenté de réaliser une attaque bien connu de la couche 2.

Retrouver **l'adresse IP réelle** de la machine malveillante et le **numéro de paquet** à l'origine de l'attaque.

**Format :** une adresse IPv4 et un numéro de paquet (ex : `MAC{X.X.X.X_numeroDePaquet}`)

Exemple : `MAC{192.168.1.1_42}`
