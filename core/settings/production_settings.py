from core.settings.base_settings import *  # NOQA isort:skip

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres-db-service",  # set in docker-compose.yml and K8s service
        "PORT": 5432,  # default postgres port
    }
}
