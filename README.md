# Projet Django - Commandes
`skyflow C:up` : run project

`skyflow C:django:logs` : see Django logs

`skyflow C:django:bash` : connect to Django container’s bash

Generate migration files :

```bash
skyflow C:django:bash
python manage.py makemigrations
```

To perform DB migrations :

```bash
skyflow C:django:bash
python manage.py migrate
```

Run Cards fixture :

```bash
skyflow C:django:bash
python manage.py loaddata card
```

## Troubleshooting

If Django bash console says `yaml/crispy-forms not found`, run these commands :
```bash
skyflow C:django:bash
pip install pyyaml
pip install django-crispy-forms
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

## Create admin user
```bash
skyflow C:django:bash
python manage.py createsuperuser --username=joe --email=joe@example.com
# then you are prompted to enter user password
```

Then visit http://localhost:8000/admin

#esgi/python

## Cards images

Cards images are stored on Cloudinary ; names and picture files taken from www.hearthpwn.com/cards
