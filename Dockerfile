ARG PYTHON_VERSION=3.11.5-slim-bullseye

# define an alias for the specific python version used in this file.
FROM python:${PYTHON_VERSION} as python
LABEL authors="piwero"

ARG APP_HOME=/app
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  curl \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_HOME}

#copy poetry files
COPY pyproject.toml ./

RUN pip install .

# copy application code to WORKDIR
COPY . .