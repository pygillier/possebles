from pydantic import (BaseSettings, RedisDsn, PostgresDsn, Field)


class AppSettings(BaseSettings):

    debug: bool = False
    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgresql://user:pass@localhost:5432/foobar'

    class Config:
        env_prefix = "pbl_"


# Init settings
app_settings = AppSettings()
