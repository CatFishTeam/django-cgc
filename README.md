# Projet Django - Commandes
`skyflow C:up` : run project

`skyflow C:django:logs` : see Django logs

`skyflow C:django:bash` : connect to Django container’s bash


To perform DB migrations :

```
skyflow C:django:bash
python manage.py migrate
```

## Ports
:8000 : web app

:8080 : Adminer (manage Postgres DB)

:5432 : Postgresql


## Adminer access (default by Skyflow)
Host : <postgres container name (see docker-compose file)>

User : skyflow

Password : root
 
Database : skyflow



#esgi/python
