# CRUD App with GitHub Authentication

A modern Django application for user management with GitHub OAuth integration. Users can create, read, update, and delete personal and professional information. GitHub authentication enables seamless social sign-up and login.

## Quick Start

### Prerequisites

- **Python 3.12+**
- **uv** (fast Python package manager) — [install here](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Clone & Setup

```bash
git clone <repository>
cd crud_auth_github

# Create virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv sync
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If available
# OR create manually:
touch .env
```

Add the following to `.env`:

```ini
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# GitHub OAuth (optional for local development)
GH_CLIENT_ID=your_github_client_id
GH_CLIENT_SECRET=your_github_client_secret
```

> **Note**: For local testing without GitHub OAuth, leave `GH_CLIENT_ID` and `GH_CLIENT_SECRET` empty—they have safe defaults.

### 3. Setup GitHub OAuth (Optional)

To enable GitHub authentication in your app:

1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Click "Register a new application"
3. Fill in:
   - **Application name**: Your app name
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/accounts/github/login/callback/`
4. Copy the **Client ID** and **Client Secret** to your `.env` file

### 4. Run the Application

```bash
# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start the development server
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## Development

### Project Structure

```
crud_auth_github/
├── accounts/               # User authentication & profiles
│   ├── models.py          # CustomUser model
│   ├── views.py           # Authentication views
│   ├── forms.py           # User forms
│   └── urls.py            # Account URLs
├── core/                  # Django core config
│   ├── settings/          # Environment-specific settings
│   ├── urls.py            # Main URL router
│   └── wsgi.py / asgi.py  # WSGI/ASGI entry points
├── tests/                 # Test suite (21 tests, 100% pass)
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── manage.py              # Django CLI
└── pyproject.toml         # Project config (dependencies, tools)
```

### Code Quality & Type Checking

This project uses modern Python tooling:

- **ty** — Fast type checker (replaces mypy)
- **ruff** — Unified linter & formatter (replaces black + isort)
- **uv** — Fast package manager (replaces poetry)

#### Run Quality Checks

```bash
# Type checking
.venv/bin/ty check .

# Linting
.venv/bin/ruff check .

# Code formatting
.venv/bin/ruff format .

# Format check (without modifying)
.venv/bin/ruff format . --check
```

#### Pre-commit Hooks

Set up git hooks to run checks automatically before commit:

```bash
# Install pre-commit
uv pip install pre-commit

# Setup hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

This ensures all code is formatted, typed, and linted before pushing.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=accounts --cov=core

# Run specific test file
pytest tests/accounts/test_accounts.py

# Run with verbose output
pytest -v

# Run in parallel (faster)
pytest -n auto
```

**Current test coverage**: 21 tests covering:
- User signup and login (django-allauth)
- User profile editing
- Form validation
- Template rendering

### Project Features

✅ **Django 6.0.7** — Latest stable Django  
✅ **PostgreSQL ready** — Uses django-allauth  
✅ **GitHub OAuth** — Social authentication via allauth  
✅ **Type-checked** — Full type annotations with ty  
✅ **Fully formatted** — Consistent code style with ruff  
✅ **Well-tested** — 21 passing tests, pytest + coverage  
✅ **Modern stack** — uv, ty, ruff, pytest  
✅ **Docker ready** — docker-compose.yml included  
✅ **Kubernetes ready** — k8s manifests in `/kubernetes`

### Common Development Tasks

#### Create a new Django app

```bash
python manage.py startapp myapp
```

#### Make database changes

```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

#### Access Django shell

```bash
python manage.py shell
```

#### Debug with ipdb

```python
# In your code
import ipdb; ipdb.set_trace()
```

Then interact with the debugger in your terminal.

---

## Deployment

### Option 1: Docker Compose

**Easiest way to run locally with PostgreSQL:**

```bash
# Start services (Django + PostgreSQL)
docker compose up -d

# Run migrations (first time only)
make migrate

# Create superuser (first time only)
make createsuperuser

# Collect static files
make collectstatic

# View logs
docker compose logs -f
```

**URLs:**
- Application: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`

### Option 2: Local Development (SQLite)

Perfect for local development without Docker:

```bash
python manage.py migrate
python manage.py runserver
```

**URLs:**
- Home: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`
- Signup: `http://localhost:8000/accounts/signup/`
- Login: `http://localhost:8000/accounts/login/`

### Option 3: Production with Gunicorn

```bash
# Install gunicorn (already in dependencies)
gunicorn core.wsgi:application --bind 0.0.0.0:8000

# With environment variables
DEBUG=False SECRET_KEY=your-key gunicorn core.wsgi:application
```

### Option 4: Kubernetes (K8s/K3s)

For production deployments, Kubernetes manifests are in `/kubernetes`.

#### Quick K8s Deploy

```bash
# Create namespace and secrets
kubectl apply -f kubernetes/app/
kubectl -n crud-app create secret generic django-secrets \
  --from-literal=SECRET_KEY="your_django_key" \
  --from-literal=GH_CLIENT_ID="your_github_client_id" \
  --from-literal=GH_CLIENT_SECRET="your_github_client_secret"

# Deploy database
kubectl apply -f kubernetes/app/Postgres

# Deploy Django app
kubectl apply -f kubernetes/app/django
```

#### K3s (Lightweight Kubernetes)

For self-hosted deployments on a single machine:

```bash
# Install K3s
sudo k3s kubectl get nodes

# Deploy with Cloudflare tunnel (optional)
kubectl apply -f kubernetes/cloudflare/namespace.yaml 
kubectl apply -f kubernetes/cloudflare/deployment.yaml
```

#### GCP with External Secrets

See `/kubernetes/external-secrets/` for GCP Secret Manager integration with Kustomize and Helm.

---

## Troubleshooting

### Issue: `SECRET_KEY not found` error

**Solution**: Create `.env` file with `SECRET_KEY=your-secret-key-here`

### Issue: `ModuleNotFoundError: No module named 'django'`

**Solution**: Run `uv sync` to install dependencies

### Issue: Database migrations fail

**Solution**: 
```bash
python manage.py migrate --run-syncdb  # Force syncdb
python manage.py migrate               # Then migrate
```

### Issue: Static files not loading in browser

**Solution**: 
```bash
python manage.py collectstatic --noinput
```

### Issue: Tests fail with authentication errors

**Solution**: Ensure test settings use SQLite:
```bash
DJANGO_SETTINGS_MODULE=core.settings.test_settings pytest
```

---

## Contributing

### Before Committing

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix

# Type check
ty check .

# Run tests
pytest

# Pre-commit hooks
pre-commit run --all-files
```

### Code Style

- **Type hints**: All functions should have return types
- **Formatting**: 88 character line length (ruff)
- **Linting**: E, F, I rules (ruff)
- **Tests**: 100% pass rate required

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | Django | 6.0.7 |
| **Database** | PostgreSQL / SQLite | Latest |
| **Auth** | django-allauth | 65.18.0 |
| **Type Checker** | ty | 0.0.63+ |
| **Linter/Formatter** | ruff | 0.16.0+ |
| **Package Manager** | uv | 0.11.32+ |
| **Testing** | pytest | 9.1.1+ |
| **Web Server** | Gunicorn | 26.0.0+ |
| **Container** | Docker | Latest |

---

## Project Info

- **Author**: Piwero
- **Python**: 3.12+
- **License**: See LICENSE file
- **Tests**: 21 passing tests
- **Type Coverage**: 100% (ty check passes)

---

## Quick Links

- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Docs](https://django-allauth.readthedocs.io/)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [ruff Linter](https://docs.astral.sh/ruff/)
- [ty Type Checker](https://github.com/astral-sh/ty)
