"""Parse Config"""

import configparser
import os


config = configparser.ConfigParser()
config.read(os.environ.get("SETTINGS_FILE") or "settings.ini")

database_connection_string = os.path.expandvars(
    config.get("database", "database_connection_string")
)
