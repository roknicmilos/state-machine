"""Logging via Loguru. Use get_logger(__name__) for a module-scoped logger."""

import os
import sys
from typing import TYPE_CHECKING

from loguru import logger as _loguru_logger

if TYPE_CHECKING:
    from loguru import Logger

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Remove default handler and add one with consistent format
_loguru_logger.remove()
_loguru_logger.add(
    sys.stdout,
    format='[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {extra[name]}: {message}',
    level=LOG_LEVEL,
)


def get_logger(name: str) -> 'Logger':
    """Return a Loguru logger bound with the given name (usually __name__)."""
    return _loguru_logger.bind(name=name)
