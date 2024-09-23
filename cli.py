# cli.py
import click
import uvicorn
import os

@click.group()
def cli():
    """CLI for managing the FastAPI server."""
    pass

@cli.command()
def start():
    """Start the FastAPI server."""
    # Importing here to avoid circular dependencies if needed
    from src.orchestrate.server.main import app

    # Change the working directory to the directory where cli.py is located
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    # Start the Uvicorn server programmatically
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    cli()
