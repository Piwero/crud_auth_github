# CRUD app with Github authentication 
https://crud-app-github.herokuapp.com/

## Getting started:

---
This app allows user to create, read, update and delete personal and professional information about the user. User can sign up with its Github account. 


## Set up

---
In order to run this project, clone this repository on you local. Then, follow the following steps:

### Create and activate virtualenv
```commandline
virtualenv .venv -p python3
. .venv/bin/activate
```

### Install requirements
```commandline
pip install Poetry
poetry install
```

### Secret keys
python-decouple has been used for hiding secrets and keys of this project. You can create a local .env file with the following command and structure.

```commandline
touch .env
```
**.env**:
```

#Django SECRETS

SECRET_KEY='###'

DEBUG=False

DATABASE_URL=sqlite:///db.sqlite3

#GitHub SECRETS

GH_CLIENT_ID="###"
GH_CLIENT_SECRET="###"


``` 
Secrets are hidden in order to preserve the security of the project, ask the author for this information.

### Run migrations to create models in a SQL DB.
```commandline
python manage.py migrate
```

### Collect Statics to serve additional files such as images, JavaScript, or CSS.
```commandline
python manage.py collectstatic
```

## Run server

```commandline
python manage.py runserver
```

### Run tests

#### Backend
```commandline
python manage.py test
```
