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


## option 3A deploy app passing secrets
```commandline
kubectl apply -f kubernetes/app/
kubectl -n crud-app create secret generic django-secrets --from-literal=SECRET_KEY="your_django_key" --from-literal=GH_CLIENT_ID="your_github_client_id" --from-literal=GH_CLIENT_SECRET="your-github_client_secret"
```
Change match route from kubernetes/app/django/ingress-route.yaml
```commandline
kubectl apply -f kubernetes/app/Postgres
kubectl apply -f kubernetes/app/django
```

## option 3B - Self hosted with K3s
### Install K3s (Very lightweight for small projects)
`sudo k3s kubectl get nodes`
`sudo k3s kubectl get pods -A`
and check pods health

### Create tunnel
Create tunnel on cloudflare and get token. 
Use http and `kubectl get services -A` to get namespace add on cloudflare on Public hostname `namespace.name` like `HTTP://kube-system.traefik` 

Create cloudflared/traefik tunnel
```
kubectl apply -f kubernetes/cloudlfare/namespace.yaml 
kubectl apply -f kubernetes/cloudlfare/deployment.yaml
```

Pass cloudflare tunnel token as secret
#### Opcion A - Pass secrets directly
```commandline
kubectl -n cloudflare create secret generic cloudflare-secrets --from-literal=TUNNEL_TOKEN="your_cloudflare_tunnel_token" 
kubectl apply -f kubernetes/cloudflare
```

#### Opcion B - Use external secrets

# Instructions


### 1. Install requirements

### gcloud-cli

 https://cloud.google.com/sdk/docs/install#installation_instructions

or https://stackoverflow.com/questions/23247943/trouble-installing-google-cloud-sdk-in-ubuntu

### Kustomize

`brew install kustomize`

### Helm

https://helm.sh/docs/intro/install/

### 2. Login

`gcloud auth login`

### 3. Define common variables

This is optional but helps to avoid typos

Copy values from `kubernetes/external-secrets/.env`

```bash
PROJECT=my-project-name #piwero-secrets
SA_NAME=gke-service-account-dev #Service Account to be created
```

### 4. Create a GCP service account

```bash
gcloud iam service-accounts create ${SA_NAME} --project ${PROJECT} --display-name="Service account for GKE"

gcloud projects add-iam-policy-binding ${PROJECT} \
    --member="serviceAccount:${SA_NAME}@${PROJECT}.iam.gserviceaccount.com" \
    --project ${PROJECT} \
    --role="roles/secretmanager.secretAccessor"
```

### 5. Generate GCP Service account secret in kubernetes

```bash
KEY_FILE=gcp-creds.json
SA=${SA_NAME}@${PROJECT}.iam.gserviceaccount.com
SECRET=gcp-secret-manager
NS=external-secrets

kubectl create namespace ${NS}

# Create service account secret
gcloud iam service-accounts keys create ${KEY_FILE} --iam-account=${SA}
kubectl delete secret ${SECRET} -n ${NS}
kubectl create secret generic ${SECRET} --from-file=${KEY_FILE}=${KEY_FILE} -n ${NS}

# Remove creds.json file
rm ${KEY_FILE}
```

### 6. Create vault in GCP

```bash
VAULT_NAME=test_vault
gcloud secrets --project ${PROJECT} create ${VAULT_NAME} --replication-policy="automatic"

```

### 7. Add secrets (json format) to vault

The next step will create version 1 of secrets the first time, and will create a new version every time this is run, so we can use different version of secrets on different environments

```bash
cat << EOF | gcloud secrets --project ${PROJECT} versions add ${VAULT_NAME} --data-file=-
{

  "SECRET_KEY": "XXXX",
  "GH_CLIENT_ID": "XXX",
  "GH_CLIENT_SECRET": "XXX",
}
EOF
```

## Use of secrets

### 8.  Install kustomize in your mac

`brew install kustomize`

### 9. Copy folder of components

`k8s/apps/base/system/external-secrets`

### 10. Edit your project id

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: gcp-secret-store
spec:
  provider:
    gcpsm:
      projectID: ${PROJECT} # This is the GCP project that Secret Manager is used
      auth:
        secretRef:
          secretAccessKeySecretRef:
            namespace: external-secrets           # Namespace of Secret contains GCP service account
            name: gcp-secret-manager    # Name of the K8s Secret you want
            key: gcp-creds.json  
```

### 11.  Inject secrets to app deployment

```yaml
spec:
      containers:
      - name: xxx
        image: xxx
        imagePullPolicy: Always
			env:
        - name: GH_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: gcp-secret-manager
              key: GH_CLIENT_ID
```

### 13.  Apply overall external secrets

```bash
kubectl kustomize kubernetes/external-secrets/. --enable-helm | kubectl apply -f -
```
