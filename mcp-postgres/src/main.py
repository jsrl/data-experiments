"""Main entry point for the Postgres MCP Server."""
import logging
import sys

from config import DatabaseConfig
from models import ExitCode
from server import PostgresMCPServer
from utils.logging import setup_logging

logger = logging.getLogger(__name__)


def main() -> int:
    """Main application entry point."""
    setup_logging()

    try:
        logger.info("Loading configuration...")
        config = DatabaseConfig.from_environment()

        server = PostgresMCPServer(config)
        server.run()

        return ExitCode.SUCCESS.value

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return ExitCode.CONFIGURATION_ERROR.value

    except (KeyboardInterrupt, SystemExit):
        logger.info("Received shutdown signal (Ctrl+C)")
        return ExitCode.SUCCESS.value

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return ExitCode.UNEXPECTED_ERROR.value


if __name__ == "__main__":
    sys.exit(main())
