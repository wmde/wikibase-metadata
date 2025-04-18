"""Parse Config"""

import configparser
import os


config = configparser.ConfigParser()
config.read(os.environ.get("SETTINGS_FILE") or "settings.ini")

database_connection_string = os.path.expandvars(
    config.get("database", "database_connection_string")
)
jobs_db_connection_string = os.path.expandvars(
    config.get(
        "database",
        "jobs_db_connection_string",
        fallback=database_connection_string.replace("wikibase-data.db", "jobs.db"),
    )
)

log_directory = os.path.expandvars(
    config.get("logging", "log_directory", fallback="logs")
)
log_level = config.get("logging", "log_level", fallback="INFO")
