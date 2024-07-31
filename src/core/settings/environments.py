"""
Environment values
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings import BASE_DIR


class ApiEnvs(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=BASE_DIR / '../environments/.env', env_nested_delimiter='__')


envs = Envs()  # type: ignore
