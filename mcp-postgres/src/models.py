"""Data models and enums."""
from enum import Enum


class ExitCode(Enum):
    """Application exit codes."""
    SUCCESS = 0
    CONFIGURATION_ERROR = 1
    DATABASE_ERROR = 2
    UNEXPECTED_ERROR = 3
