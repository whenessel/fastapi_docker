import os
from logging.config import fileConfig

from alembic import context
from app.db import Base, metadata
from dotenv import load_dotenv
from sqlalchemy import MetaData, engine_from_config, pool, text
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_engine_from_config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
load_dotenv("./app/.env")
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USERNAME"))
config.set_section_option(section, "DB_PASS", os.environ.get("DB_PASSWORD"))

if os.environ.get("APP_ENV") == "local":
    config.set_section_option(section, "DB_HOST", "localhost")
else:
    config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST"))

config.set_section_option(section, "DB_DATABASE", os.environ.get("DB_DATABASE"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None


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
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
    print("Tenant 2 : ", current_tenant)
    dry_run = context.get_x_argument(as_dictionary=True).get("dry_run")
    print("Dry Run : ", dry_run)
    session = Session(bind=connection)
    session.execute(text('set search_path to "%s"' % current_tenant))

    # add this line
    connection.commit()

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=current_tenant,
    )

    with context.begin_transaction() as transaction:
        context.run_migrations()
        if bool(dry_run) == True:
            print("Dry-run succeeded; now rolling back transaction...")
            transaction.rollback()


async def run_async_migrations():

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
    print("Tenant 1 : ", current_tenant)

    async with connectable.connect() as connection:
        await connection.execute(text('set search_path to "%s"' % current_tenant))
        connection.dialect.default_schema_name = current_tenant

        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    print("Running migrations online")
    connectable = config.attributes.get("connection", None)
    print("Connectable ::: ", connectable)
    # connectable = None
    if connectable is None:
        asyncio.run(run_async_migrations())
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()