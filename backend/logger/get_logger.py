"""Logger"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

from config import log_directory, log_level
from logger.extra_formatter import OptionalExtraFormatter


os.makedirs(f"{log_directory}/{log_level.lower()}", exist_ok=True)
os.makedirs(f"{log_directory}/error", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

wikibase_formatter = OptionalExtraFormatter()

file_handler = TimedRotatingFileHandler(
    f"{log_directory}/{log_level.lower()}/suite-scraper.log",
    encoding="utf-8",
    when="midnight",
    utc=True,
)
file_handler.setLevel(log_level.upper())
file_handler.setFormatter(wikibase_formatter)
logger.addHandler(file_handler)

file_error_handler = TimedRotatingFileHandler(
    f"{log_directory}/error/suite-scraper-error.log",
    encoding="utf-8",
    when="w5",
    utc=True,
)
file_error_handler.setLevel(logging.WARNING)
file_error_handler.setFormatter(wikibase_formatter)
logger.addHandler(file_error_handler)

# debug level logs to stdout, no matter what log level is set
# makes sure that you always see the logs in the console
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(wikibase_formatter)
logger.addHandler(stdout_handler)
