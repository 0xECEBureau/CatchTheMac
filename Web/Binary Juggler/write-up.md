La page permet à un utilisateur de se connecter.

Parmi les informations à comprendre sur le site, les points intéressants sont :

- L'extension de la page, c'est donc du PHP
- Le message parle de hashage de mot de passe en MD5
- Le mot de passe recherché est celui de l'admin

En regroupant ces informations avec celles de l'énoncé, notamment le titre qui parle de binary juggler, des recherches s'imposent.

**Hacktricks** et **PayloadAllTheThings** sont des sites bien connus de l'exploitation Web et compilent la plupart des failles connues.

La page https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md semble intéressante. Le type juggling permet de convertir des données implicitement lors de comparaisons permettant à des valeurs qui ne sont pas égales de réussir la comparaison.

Dans les magic hashs, en MD5, si le password est égale à `0e215962017` alors il sera égale à `0e291242476940776845150308577824` une fois haché. La valeur entrée sera ainsi convertit en nombre en écriture scientifique du fait du type juggling et sera égale à 0. Il est possible que le mot de passe de l'administrateur soit alors aussi égale à 0 selon les indices.

En testant ce mot de passe avec le nom d'utilisateur admin, l'authentification est validée et le flag est obtenu.
