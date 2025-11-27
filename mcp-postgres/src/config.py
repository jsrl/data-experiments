"""Configuration management for the Postgres MCP Server."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class DatabaseConfig:
    """Immutable database configuration."""
    host: str
    port: int
    database: str
    user: str
    password: str

    @classmethod
    def from_environment(cls) -> 'DatabaseConfig':
        """
        Create configuration from environment variables.

        Environment variables:
            - DB_HOST (required)
            - DB_PORT (default: 5432)
            - DB_NAME (required)
            - DB_USER (required)
            - DB_PASSWORD (required)

        Returns:
            DatabaseConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        try:
            return cls(
                host=os.environ['DB_HOST'],
                port=int(os.getenv('DB_PORT', '5432')),
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid database configuration: {e}") from e


    def get_masked_dsn(self) -> str:
            """Get connection string with masked password for logging."""
            return f"{self.user}:***@{self.host}:{self.port}/{self.database}"

    def to_connection_params(self) -> dict:
            """Get connection parameters for asyncpg."""
            return {
                'host': self.host,
                'port': self.port,
                'database': self.database,
                'user': self.user,
                'password': self.password
            }
