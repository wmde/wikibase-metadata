"""Parse Config"""

import configparser
import os


config = configparser.ConfigParser()
config.read(os.environ.get("SETTINGS_FILE", "settings.ini"))

auth_token = os.path.expandvars(config.get("auth", "auth_token"))
assert auth_token is not None, "No Authentication Token Found"

database_connection_string = os.path.expandvars(
    config.get("database", "database_connection_string")
)

deactivate_scheduler = config.getboolean("scheduler", "deactivate", fallback=False)

log_directory = os.path.expandvars(
    config.get("logging", "log_directory", fallback="logs")
)
log_level = config.get("logging", "log_level", fallback="INFO")
