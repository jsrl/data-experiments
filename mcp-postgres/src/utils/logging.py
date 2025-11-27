"""Logging configuration."""
import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure application logging.

    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
