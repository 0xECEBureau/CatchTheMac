# CatchTheMac

Ce repo contient l'ensemble des ressources pour le CTF CatchTheMac.

## Lore

L’histoire d’0xECE est jalonnée de mystères, mais aucun n’est aussi troublant que la disparition de Mac. Ancien membre respecté du groupe, il a brusquement quitté la scène sans prévenir. Officiellement, il a pris sa retraite. Officieusement, les rumeurs disent qu’il est parti avec des secrets bien trop précieux pour être laissés entre de mauvaises mains.

Certains affirment qu’il a effacé toute trace de son existence. D’autres prétendent qu’il a semé des indices dans des challenges, comme un dernier jeu avant de disparaître définitivement. Pourquoi ? Personne ne le sait. Ce qui est certain, c’est que ces challenges contiennent des fragments de vérité, dissimulés derrière du code, des chiffres et des algorithmes tordus.

Votre mission est simple en apparence : retrouver Mac et récupérer ce qu’il a volé. Mais Mac n’est pas du genre à se laisser traquer facilement. Il a laissé derrière lui un enchaînement d’épreuves conçues pour tester les meilleurs. Seuls ceux qui sauront décrypter ses messages, déjouer ses pièges et suivre ses traces pourront espérer découvrir la vérité.

## Contenu du CTF

Ce CTF s'adresse au membre d'0xECE de niveau grand débutant à confirmé. Le but est de découvrir les grandes catégories du CTF et de trouver le niveau de difficulté qui vous correspond le mieux.

L'objectif de chaque challenge est de retrouver un flag au format `MAC{X}`. Certain challenges vous demanderont de retrouver une information précise et de la concaténer avec le format du flag, tout vous sera précisé dans l'énoncé du challenge.

## Structure

Pour chaque challenge, veuillez respecter la strucutre suivante :

```
categorie/
    nom_du_challenge/
        README.md => Description du challenge, énoncé et flag format
        WU.md => Write-up du challenge
        resources/ => Dossier contenant les ressources à fournir aux joueurs
        sources/ => Dossier contenant le source code du challenge
        fichier_donnees
        fichier_donnees
        ...
```

Pour chaque challenge si des ressources doivent être fournies (fichiers, scripts, etc.), veuillez les placer dans un dossier nommé `resources`.
