import logging
import sys

import structlog

from src.config import settings


def configure_logger():
    """
    Configures structlog to work with Python's standard logging.
    - Uses colorful human-readable output if running in a terminal (TTY).
    - Uses JSON output if running in Docker/Production (non-TTY).
    """

    # 1. Set the log level from config
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.LOG_LEVEL.upper(),
    )

    # 2. Define shared processors (timestamps, log level, etc.)
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # 3. Decide renderer based on environment (Console vs Docker)
    if sys.stderr.isatty():
        # Pretty colors for local development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        # JSON for Docker/Production tools (Datadog, Grafana, etc.)
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]

    # 4. Apply configuration
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
