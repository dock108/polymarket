from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field(default="Polymarket Edge API")

    class Config:
        env_file = ".env"
        extra = "ignore"
