"""Logger"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os

from config import log_level

DEFAULT_ARGS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "wikibase",
}


class OptionalExtraFormatter(logging.Formatter):
    """Supports an optional `wikibase` extra argument"""

    def format(self, record: logging.LogRecord) -> str:
        """Format Record"""

        base_fmt = "%(asctime)s | %(levelname)s | %(message)s"
        wikibase_fmt = (
            "%(asctime)s | %(levelname)s | wikibase %(wikibase)d | %(message)s"
        )

        if "wikibase" in record.__dict__.keys():
            self._style._fmt = wikibase_fmt  # pylint: disable=protected-access
        else:
            self._style._fmt = base_fmt  # pylint: disable=protected-access

        for k in record.__dict__.keys():
            if k not in DEFAULT_ARGS:
                self._style._fmt += f"\n\t{k}: {record.__dict__.get(k)}"

        return super().format(record)


os.makedirs(f"logs/{log_level.lower()}", exist_ok=True)
os.makedirs("logs/error", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

wikibase_formatter = OptionalExtraFormatter()

file_handler = TimedRotatingFileHandler(
    f"logs/{log_level.lower()}/suite-scraper.log",
    encoding="utf-8",
    when="midnight",
    utc=True,
)
file_handler.setLevel(log_level.upper())
file_handler.setFormatter(wikibase_formatter)
logger.addHandler(file_handler)

file_error_handler = TimedRotatingFileHandler(
    "logs/error/suite-scraper-error.log", encoding="utf-8", when="w0", utc=True
)
file_error_handler.setLevel(logging.WARNING)
file_error_handler.setFormatter(wikibase_formatter)
logger.addHandler(file_error_handler)
