import typer
import subprocess
import os
import asyncio
from sqlalchemy import create_engine, select
from app.config import get_settings
from app.db import Base
from app.db.database import AsyncSessionLocal
from app.db.models import User

app = typer.Typer()
settings = get_settings()


@app.command()
def run():
    """Run the FastAPI application."""
    typer.echo("Starting FastAPI app...")
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])


@app.command()
def makemigrations(message: str = "Auto migration"):
    """Generate a new Alembic migration."""
    typer.echo(f"Generating migration: {message}")
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])


@app.command()
def migrate():
    """Apply all pending Alembic migrations."""
    typer.echo("Applying migrations...")
    subprocess.run(["alembic", "upgrade", "head"])


@app.command()
def downgrade(revision: str = "-1"):
    """Rollback the last Alembic migration (default: one step)."""
    typer.echo(f"Rolling back to {revision}...")
    subprocess.run(["alembic", "downgrade", revision])


@app.command()
def db_status():
    """Show current database migration status."""
    typer.echo("Checking Alembic migration status...")
    subprocess.run(["alembic", "current"])


async def _create_superuser_async(email: str, username: str, password: str):
    """Async helper to create a superuser."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(User).where((User.email == email) | (User.username == username))
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                if existing_user.email == email:
                    typer.secho(
                        f"Error: User with email '{email}' already exists.",
                        fg=typer.colors.RED,
                        err=True,
                    )
                    return
                if existing_user.username == username:
                    typer.secho(
                        f"Error: User with username '{username}' already exists.",
                        fg=typer.colors.RED,
                        err=True,
                    )
                    return

            new_user = User(
                email=email,
                username=username,
                is_superuser=True,
                role="admin",
                is_active=True,
                email_verified=True,  # Superusers created via CLI can be considered verified
            )
            new_user.set_password(password)
            session.add(new_user)

            typer.secho(
                f"Superuser '{username}' created successfully with email '{email}'.",
                fg=typer.colors.GREEN,
            )


@app.command()
def createsuperuser(
    email: str = typer.Option(..., prompt=True, help="The email address for the superuser."),
    username: str = typer.Option(..., prompt=True, help="The username for the superuser."),
    password: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="The password for the superuser.",
    ),
):
    """Creates a new superuser with admin privileges."""
    typer.echo("Creating superuser...")
    try:
        asyncio.run(_create_superuser_async(email, username, password))
    except Exception as e:
        typer.secho(
            f"An error occurred during superuser creation: {e}", fg=typer.colors.RED, err=True
        )


if __name__ == "__main__":
    app()
