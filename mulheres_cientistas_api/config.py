from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
