# CRUD app with Github authentication 

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

To begin with the application, in your GitHub account. Follow these steps:

1. Go to your profile and click on "Settings."
2. Scroll down and select "Developer Settings" from the left-hand side menu.
3. Choose "OAuth Apps."
4. Click on "Register a new application."
5. Fill in the following details:
   - Application Name: test
   - Homepage URL: http://localhost:8000
   - Authorization callback URL: http://localhost:8000/accounts/github/login/callback/
6. Click "Register Application."
7. Generate the client secret code.
8. Copy the client ID and client secret, then paste them here (.env file or GH secrets):
   SOCIAL_AUTH_GITHUB_KEY = '############'
   SOCIAL_AUTH_GITHUB_SECRET = '########################'

Secrets are hidden in order to preserve the security of the project, ask the author for this information.

# Option 1 - Docker Compose Setup

### Build containers
```commandline
docker compose up -d
```
## Only first time
### Run migrations
```commandline
make migrate
```
### Create user
```commandline
make createsuperuser
```
### Collect Static (if not showing logo on lading page)
```commandline
make collectstatic
```

# Option 2 - Local Setup

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
# Urls
- [Home](http://localhost:8000)
- [Admin](http://localhost:8000/admin)

# option 3 - K8s Setup


## Deploy app
```commandline
kubectl apply -f kubernetes/app/
kubectl -n crud-app create secret generic django-secrets --from-literal=SECRET_KEY="your_django_key" --from-literal=GH_CLIENT_ID="your_github_client_id" --from-literal=GH_CLIENT_SECRET="your-github_client_secret"
# change match route from kubernetes/app/django/ingress-route.yaml
kubectl apply -f kubernetes/app/postgres
kubectl apply -f kubernetes/app/django
```

## Create cloudflare tunnel
```commandline
kubectl -n cloudflare create secret generic cloudflare-secrets --from-literal=TUNNEL_TOKEN="your_cloudflare_tunnel_token" 
kubectl apply -f cloudflare
```
