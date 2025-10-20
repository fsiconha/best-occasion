from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration managed via environment variables."""

    environment: str = "development"
    vector_store_url: str | None = None
    embedding_model_name: str = "intfloat/e5-small-v2"
    embedding_instruction: str = (
        "Represent the digital recommendation occasion for retrieval:"
    )

    model_config = SettingsConfigDict(
        env_prefix="BEST_OCCASION_",
        env_file=".env",
    )


def get_settings() -> Settings:
    """Return cached settings instance for dependency injection."""

    return Settings()  # type: ignore[call-arg]
