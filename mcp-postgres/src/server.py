"""MCP server implementation."""
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from config import DatabaseConfig
from database import DatabaseConnectionPool

logger = logging.getLogger(__name__)

class PostgresMCPServer:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        # Initialize pool but don't connect yet
        self.pool = DatabaseConnectionPool(config)

        @asynccontextmanager
        async def lifespan(server: FastMCP) -> AsyncIterator[None]:
            """Manages startup and shutdown logic inside the Server's loop."""
            try:
                logger.info("Initializing Database Pool...")
                await self.pool.initialize()

                if not await self.pool.health_check():
                    logger.error("Health check failed on startup!")
                else:
                    logger.info("Database connected successfully")

                yield # Server runs here

            except (KeyboardInterrupt, SystemExit):
                logger.info("Received shutdown signal")
            finally:
                logger.info("Closing Database Pool...")
                await self.pool.close()
                logger.info("Shutdown complete")

        # 2. Pass lifespan to FastMCP
        self.mcp = FastMCP("Postgres Database Server", lifespan=lifespan)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Register MCP tool handlers."""

        @self.mcp.tool()
        async def list_tables() -> str:
            """List all public tables in the database."""
            sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(sql)
                return str([row['table_name'] for row in rows])

        @self.mcp.tool()
        async def describe_table(table_name: str) -> str:
            """Get the schema for a specific table."""
            sql = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = $1
            """
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(sql, table_name)
                return str([dict(row) for row in rows])

        @self.mcp.tool()
        async def query_database(query: str) -> str:
            """
            Run a read-only SQL query to fetch data.
            PRIMARY method for data access. ALWAYS use this tool for SELECT queries.

            Args:
                query: A valid SQL SELECT statement (e.g., "SELECT * FROM pokemon LIMIT 5").
            """
            # Basic safety: Reject non-SELECT queries to prevent accidental data modification
            if not query.strip().upper().startswith("SELECT"):
                return "Error: Only SELECT statements are allowed via this tool."

            try:
                async with self.pool.acquire() as conn:
                    rows = await conn.fetch(query)

                    if not rows:
                        return "Query executed successfully but returned no results."

                    results = [dict(row) for row in rows]

                    # OPTIONAL: Safety limiter for Context Window
                    # If the result is huge (>100 rows), truncate
                    if len(results) > 100:
                        return str(results[:100]) + f"\n... (Truncated. {len(results)} total rows. Add 'LIMIT' to your query.)"

                    return str(results)

            except Exception as e:
                return f"Database Error: {str(e)}"

    def run(self) -> None:
        """Start the server (Blocking Call)."""
        # No asyncio.run() needed here! FastMCP handles it.
        self.mcp.run()
