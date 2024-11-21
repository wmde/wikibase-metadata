"""Logger"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os

from config import log_level
from logger.extra_formatter import OptionalExtraFormatter


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
