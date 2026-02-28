from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file="./../.env", extra="ignore"
    )
    api_key: str = Field(alias="LIVEKIT_API_KEY")
    api_secret: str = Field(alias="LIVEKIT_API_SECRET")
    server_url: str = Field(alias="LIVEKIT_URL")


settings = Settings(**{})
