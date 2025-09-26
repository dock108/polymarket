from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="Polymarket Edge API", description="Application name")
    # Default for local dev (run from backend/) writes under repo data/
    database_url: str = Field(default="sqlite:///../data/dev.db", alias="DATABASE_URL")
    odds_api_key: str | None = Field(default=None, alias="ODDS_API_KEY")
    datagolf_api_key: str | None = Field(default=None, alias="DATAGOLF_API_KEY")
    fee_cushion: float = Field(default=0.025, alias="FEE_CUSHION", ge=0.0, le=0.10)
    refresh_interval_seconds: int = Field(default=600, alias="REFRESH_INTERVAL_SECONDS", ge=60, le=3600)

    polymarket_base_url: str = Field(
        default="https://gamma-api.polymarket.com",
        alias="POLYMARKET_BASE_URL",
    )


settings = Settings()
