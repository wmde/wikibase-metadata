import logging
from logging.handlers import TimedRotatingFileHandler
import os

from config import log_level

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = TimedRotatingFileHandler(
    "logs/suite-scraper.log", encoding="utf-8", when="midnight", utc=True
)
file_handler.setLevel(log_level.upper())
logger.addHandler(file_handler)

file_error_handler = TimedRotatingFileHandler(
    "logs/suite-scraper-error.log", encoding="utf-8", when="w0", utc=True
)
file_error_handler.setLevel(logging.WARNING)
logger.addHandler(file_error_handler)
