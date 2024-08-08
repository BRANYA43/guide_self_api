"""
Environment values
"""

import os
from typing import Any

from pydantic import field_validator, EmailStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings import BASE_DIR


class SuperuserEnvs(BaseSettings):
    username: str | None = None
    email: EmailStr
    password: str

    @model_validator(mode='before')
    def set_django_envs(cls, data: dict[str, Any]) -> dict[str, Any]:
        for name, value in data.items():
            os.environ.setdefault(f'django_superuser_{name}'.upper(), value)
        return data


class ApiEnvs(BaseSettings):
    superuser: SuperuserEnvs
    secret_key: str
    debug: bool = False
    allowed_hosts: list[str] | str = ['*']

    @field_validator('allowed_hosts', mode='before')
    def split_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v = v.split(' ')
        return v


class Envs(BaseSettings):
    api: ApiEnvs

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / '../environments/.env'),
        env_nested_delimiter='__',
    )


envs = Envs()  # type: ignore
