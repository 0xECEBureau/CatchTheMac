# Contexte : Osef OSI ?

Avant de disparaître, Mac a laissé une trace étrange dans les entrailles du réseau de 0xECE : une série de 7 challenges, soigneusement dissimulés, chacun exploitant une couche différente du modèle OSI.

Certains pensent qu’il s’agit d’un parcours initiatique. D’autres croient que ces épreuves protègent une clef essentielle à la vérité sur sa disparition. Une chose est sûre : vous devrez maîtriser chaque couche du modèle OSI pour en sortir victorieux.

Chaque challenge débloque un indice nécessaire pour accéder au suivant. Il faudra analyser des signaux, décrypter des paquets, intercepter des requêtes, comprendre les protocoles... Mac n'a rien laissé au hasard.

## Layer 2 - On ne peut faire confiance à personne

Niveau : moyen

Maintenant que vous avez décodé le signal intercepté, vous avez une addresse MAC. Cette identité n’apparaît dans aucune documentation officielle du réseau de 0xECE.

Un enregistrement réseau a été récupéré juste avant la disparition de Mac. Des anomalies de communication ont été détectées dans la résolution ARP du réseau local. Quelqu’un a tenté de réaliser une attaque bien connu de la couche 2.

Retrouver **l'adresse IP réelle** de la machine malveillante et le **numéro de paquet** à l'origine de l'attaque. 

Format du flag : une adresse IPv4 et un numéro de paquet (ex : `MAC{X.X.X.X_numeroDePaquet}`)



