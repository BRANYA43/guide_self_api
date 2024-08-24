"""
Django Database Settings
"""

from django.conf import settings
from core.settings.environments import envs

SQLITE3 = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': settings.BASE_DIR / '../db.sqlite3',
}

POSTGRESQL = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': envs.db.name,
    'HOST': envs.db.host,
    'PORT': envs.db.port,
    'USER': envs.db.user,
    'PASSWORD': envs.db.password,
}

DATABASES = {'default': SQLITE3 if envs.api.debug and not envs.api.docker_run else POSTGRESQL}
