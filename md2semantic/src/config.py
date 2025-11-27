from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    # GitHub
    GITHUB_TOKEN: str
    GITHUB_OWNER: str = "github"
    GITHUB_REPO: str = "awesome-copilot"
    GITHUB_BRANCH: str = "main"  # <--- Added this
    MAX_FILES: int = 5

    # Logging
    LOG_LEVEL: str = "INFO"      # <--- Added this

    # Config to allow extra fields in .env without crashing
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"           # <--- Added this to fix "Extra inputs are not permitted"
    )

settings = Settings()

def get_db_url() -> str:
    """
    Construct PostgreSQL connection URL from environment settings.

    Returns:
        SQLAlchemy-compatible database URL string
    """
    return f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
