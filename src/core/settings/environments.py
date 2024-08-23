"""
Environment values
"""

from typing import Annotated

from pydantic import field_validator, EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings import BASE_DIR


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / '../environments/.env'),
        extra='allow',
    )


class ApiEnvs(_BaseSettings):
    secret_key: Annotated[str, Field(alias='DJANGO_SECRET_KEY')]
    debug: Annotated[bool, Field(False, alias='DJANGO_DEBUG')]
    allowed_hosts: Annotated[list[str], str, Field(['*'], alias='DJANGO_ALLOWED_HOST')]

    @field_validator('allowed_hosts', mode='before')
    def split_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v = v.split(' ')
        return v


class SuperuserEnvs(_BaseSettings):
    username: Annotated[str, None, Field(None, alias='DJANGO_SUPERUSER_USERNAME')]
    email: Annotated[EmailStr, Field(alias='DJANGO_SUPERUSER_EMAIL')]
    password: Annotated[str, Field(alias='DJANGO_SUPERUSER_EMAIL')]


class Envs:
    api = ApiEnvs()  # type: ignore
    superuser = SuperuserEnvs()  # type: ignore


envs = Envs
