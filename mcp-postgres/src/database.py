"""Database connection pool management."""
import logging
from contextlib import asynccontextmanager

import asyncpg

from config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseConnectionPool:
    """Manages asyncpg connection pool lifecycle."""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize the connection pool manager.

        Args:
            config: Database configuration
        """
        self.config = config
        self._pool: asyncpg.Pool | None = None

    async def initialize(self) -> None:
        """
        Initialize the connection pool.

        Raises:
            asyncpg.PostgresError: If connection fails
        """
        if self._pool is not None:
            logger.warning("Connection pool already initialized")
            return

        logger.info(f"Initializing connection pool: {self.config.get_masked_dsn()}")

        try:
            self._pool = await asyncpg.create_pool(
                **self.config.to_connection_params()
            )
            logger.info("Connection pool initialized successfully")
        except asyncpg.PostgresError as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise

    async def close(self) -> None:
        """Close the connection pool gracefully."""
        if self._pool is None:
            return

        logger.info("Closing connection pool...")
        try:
            await self._pool.close()
            self._pool = None
            logger.info("Connection pool closed")
        except Exception as e:
            logger.error(f"Error closing connection pool: {e}")
            raise

    @asynccontextmanager
    async def acquire(self):
        """
        Context manager to acquire a database connection.

        Yields:
            asyncpg.Connection

        Raises:
            RuntimeError: If pool is not initialized

        Example:
            async with pool.acquire() as conn:
                result = await conn.fetch("SELECT * FROM users")
        """
        if self._pool is None:
            raise RuntimeError("Connection pool not initialized")

        async with self._pool.acquire() as connection:
            yield connection

    async def health_check(self) -> bool:
        """
        Perform a health check on the database connection.

        Returns:
            True if healthy, False otherwise
        """
        try:
            async with self.acquire() as conn:
                await conn.fetchval("SELECT 1")
            logger.info("Database health check: OK")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    @property
    def is_initialized(self) -> bool:
        """Check if the pool is initialized."""
        return self._pool is not None
