from typing import Any

from core.settings.base_settings import *  # NOQA isort:skip

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres-db-service",
        "PORT": 5432,
    }
}
