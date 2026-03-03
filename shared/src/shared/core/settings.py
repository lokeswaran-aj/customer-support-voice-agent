from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=ROOT_DIR / ".env", extra="ignore"
    )
    database_url: str = Field(alias="DATABASE_URL")


settings = Settings()
