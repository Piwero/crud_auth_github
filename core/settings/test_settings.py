from core.settings.base_settings import *  # NOQA isort:skip

DATABASES: dict[str, dict[str, str]] = {
    "default": {"ENGINE": "django.db.backends.sqlite3"}
}
