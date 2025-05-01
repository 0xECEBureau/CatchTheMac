# Kerbe Quoi ???

Mac a tenter de s'introduire dans l'Active Directory de l'asso, il a tellement bien réussi qu'il est carrémenet remonté à celui de l'école ! Il a pris soin d'exfiltrer tout ce qu'il pouvait avec **ldap2json**. Mais il vous charge de la tâche finale, trouvez l'utilisateur vulnerable au Kerberoasting. Au kerberoskoi ???

Le flag est composé de la balise de base et du GUID de l'object active directory concerné.

**Format :** MAC{objectGUID}

Exemple : `MAC{00000000-0000-0000-0000-000000000000}`

**Auteur :** Drachh
