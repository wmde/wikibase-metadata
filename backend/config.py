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
config_old_database_connection_string_var = config.get(
    "database", "old_database_connection_string", fallback=None
)
old_database_connection_string = (
    os.path.expandvars(config_old_database_connection_string_var)
    if config_old_database_connection_string_var is not None
    else None
)

enable_scheduler = config.getboolean("scheduler", "enable", fallback=True)

log_directory = os.path.expandvars(
    config.get("logging", "log_directory", fallback="logs")
)

log_level = os.path.expandvars(config.get("logging", "log_level", fallback="INFO"))
