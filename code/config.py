from pydantic import PostgresDsn, RedisDsn, AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    rabbit_mq_url: AmqpDsn
    openai_api_key: str


settings = Settings()


TORTOISE_CONFIG = {
    'connections': {'default': str(settings.database_url)},
    'apps': {
        'models': {
            'models': ['code.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}
