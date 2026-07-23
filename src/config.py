"""Centralized application settings via pydantic-settings."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field("development", alias="APP_ENV")
    app_version: str = "0.1.0"
    app_secret_key: str = Field("change-me-in-production", alias="APP_SECRET_KEY")
    log_level: str = Field("INFO", alias="APP_LOG_LEVEL")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"], alias="CORS_ORIGINS")

    azure_openai_endpoint: str = Field("", alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field("", alias="AZURE_OPENAI_API_KEY")
    azure_openai_deployment_chat: str = Field("gpt-4o", alias="AZURE_OPENAI_DEPLOYMENT_CHAT")
    azure_openai_deployment_embedding: str = Field("text-embedding-3-large", alias="AZURE_OPENAI_DEPLOYMENT_EMBEDDING")
    azure_openai_api_version: str = Field("2024-05-01-preview", alias="AZURE_OPENAI_API_VERSION")

    azure_search_endpoint: str = Field("", alias="AZURE_SEARCH_ENDPOINT")
    azure_search_api_key: str = Field("", alias="AZURE_SEARCH_API_KEY")
    azure_search_index_finance: str = Field("finance-knowledge", alias="AZURE_SEARCH_INDEX_FINANCE")

    fabric_workspace_id: str = Field("", alias="FABRIC_WORKSPACE_ID")
    fabric_lakehouse_id: str = Field("", alias="FABRIC_LAKEHOUSE_ID")
    adls_account_name: str = Field("", alias="ADLS_ACCOUNT_NAME")
    adls_container: str = Field("finance-lakehouse", alias="ADLS_CONTAINER")
    adls_connection_string: str = Field("", alias="ADLS_CONNECTION_STRING")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
