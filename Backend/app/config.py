from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FDO-Privacy API"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///./fdo_privacy.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()