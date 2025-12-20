import asyncio
from alembic import context
from logging.config import fileConfig
from app.db import Base, get_database_url, create_engine_with_retry

# Load Alembic configuration and set up logging
config = context.config
fileConfig(config.config_file_name)

# Set the target metadata from your SQLAlchemy models
target_metadata = Base.metadata


def run_migrations_online():
    """
    Run migrations in 'online' mode with async support.
    This is a synchronous wrapper that runs async code internally.
    """
    connectable = create_engine_with_retry(get_database_url())

    # Define an async helper function to handle the connection and migration
    async def do_run_migrations_async():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    # Run the async function synchronously using asyncio.run
    asyncio.run(do_run_migrations_async())


def do_run_migrations(connection):
    """
    Configure and run migrations synchronously on the provided connection.
    """
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    Generates SQL scripts without connecting to the database.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# Determine whether to run migrations in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
