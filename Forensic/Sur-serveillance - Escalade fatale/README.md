# Sur-serveillance - Escalade fatale

**Niveau : facile**

L’accès initial n’était pas suffisant pour mener à bien l’attaque : l’intrus avait besoin des privilèges root.

En fouillant l’historique des commandes de “mac”, vous trouverez la manipulation exacte qu’il a utilisée pour s’octroyer des droits illimités sur le système.

identifiez la ligne qui lui a permis de devenir root.


**Format :** MAC{commande d'élévation de privilege}
Exemple : `MAC{nc localhost 5000}`


**Auteur :** Snaxx