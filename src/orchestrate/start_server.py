import uvicorn

def start_server():
    """Start the FastAPI server."""
    # Importing here to avoid circular dependencies if needed
    from server.main import app

    # Start the Uvicorn server programmatically
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    start_server()
