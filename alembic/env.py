import sys
import os

# Добавляем путь к проекту, чтобы импортировать настройки и модели
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

# Импортируем метаданные
from settings import settings  # настройки
from src.database.models.base import metadata as target_metadata  # ваши таблицы

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

target_metadata = target_metadata
print("Registered tables:", target_metadata.tables.keys())


def run_migrations_offline():
    url = str(settings.db_url_postgres_sync)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {},  
        url=str(settings.db_url_postgres_sync),
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
