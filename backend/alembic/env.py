from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys

# Ensure backend/ is on import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402

config = context.config

# Paths
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
repo_root = os.path.abspath(os.path.join(backend_dir, ".."))
abs_default_db_path = os.path.join(repo_root, "data", "dev.db")

# Compose DB URL
db_url = settings.database_url or f"sqlite:///{abs_default_db_path}"

# Normalize sqlite file path and ensure parent directory exists
if db_url.startswith("sqlite:///"):
    raw_path = db_url[len("sqlite:///"):]
    if raw_path != ":memory:":
        # Make absolute relative to backend_dir
        resolved = raw_path
        if not os.path.isabs(resolved):
            resolved = os.path.abspath(os.path.join(backend_dir, resolved))
        # Also handle leading ../ cases by abspath above
        os.makedirs(os.path.dirname(resolved), exist_ok=True)
        db_url = f"sqlite:///{resolved}"

config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
