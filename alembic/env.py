from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import make_url

from alembic import context

from model.database import *


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- Helper: map async URLs to sync URLs ---
def _coerce_to_sync_url(url_str: str) -> str:
    """
    Convert common async driver URLs to their sync equivalents so
    Alembic can run with a normal (blocking) SQLAlchemy engine.
    """
    if not url_str:
        return url_str
    u = make_url(url_str)
    mapping = {
        "sqlite+aiosqlite": "sqlite",
        "postgresql+asyncpg": "postgresql+psycopg",  # or just "postgresql"
        "mysql+aiomysql": "mysql+pymysql",
    }
    new_driver = mapping.get(u.drivername, u.drivername)
    return str(u.set(drivername=new_driver))

# --- URL resolution precedence ---
# 1) alembic -x db_path=...           (explicit CLI override; no env expansion)
# 2) sqlalchemy.url from alembic.ini  (with $VAR expanded)
x_args = context.get_x_argument(as_dictionary=True)
override_db_path = x_args.get("db_path")

if override_db_path:
    url = override_db_path
else:
    ini_url = config.get_main_option("sqlalchemy.url")
    if not ini_url:
        raise RuntimeError(
            "No database URL found. Provide -x db_path=... or set sqlalchemy.url in alembic.ini."
        )
    url = os.path.expandvars(ini_url)

# --- Apply coercion to ensure sync driver for Alembic ---
url = _coerce_to_sync_url(url)

config.set_section_option(config.config_ini_section, "sqlalchemy.url", url)

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = ModelBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
