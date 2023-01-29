from pydantic import (BaseSettings, RedisDsn, PostgresDsn, HttpUrl)


class AppSettings(BaseSettings):
    app_version: str = "0.1.1"
    debug: bool = False
    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgresql://user:pass@localhost:5432/foobar'

    # Access token
    token_secret_key: str
    token_expire_minutes: int = 30
    token_algorithm: str = "HS256"

    # Mastodon
    mastodon_client_key: str
    mastodon_client_secret: str
    mastodon_access_token: str
    mastodon_api_url: HttpUrl


    class Config:
        env_prefix = "pbl_"


# Init settings
app_settings = AppSettings()
