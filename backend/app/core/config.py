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

    # External keys
    odds_api_key: str | None = Field(default=None, alias="ODDS_API_KEY")
    datagolf_api_key: str | None = Field(default=None, alias="DATAGOLF_API_KEY")

    # Modeling/refresh
    fee_cushion: float = Field(default=0.025, alias="FEE_CUSHION", ge=0.0, le=0.10)
    refresh_interval_seconds: int = Field(
        default=600, alias="REFRESH_INTERVAL_SECONDS", ge=60, le=3600
    )

    # Polymarket
    polymarket_base_url: str = Field(
        default="https://gamma-api.polymarket.com",
        alias="POLYMARKET_BASE_URL",
    )

    # The Odds API
    odds_api_base_url: str = Field(
        default="https://api.the-odds-api.com/v4",
        alias="ODDS_API_BASE_URL",
    )
    odds_api_regions: str = Field(default="us", alias="ODDS_API_REGIONS")
    odds_api_markets: str = Field(default="h2h,spreads,totals", alias="ODDS_API_MARKETS")
    odds_api_bookmakers: str = Field(
        default="",
        alias="ODDS_API_BOOKMAKERS",
    )

    # DataGolf
    datagolf_base_url: str = Field(
        default="https://feeds.datagolf.com",
        alias="DATAGOLF_BASE_URL",
    )


settings = Settings()
