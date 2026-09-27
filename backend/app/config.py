from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost/civicpulse"
    redis_url: str = "redis://localhost:6379/0"
    triage_provider: str = "rules"
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
