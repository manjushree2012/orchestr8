import logging
from src.orchestrate.websocket_handler import WebSocketHandler
from src.orchestrate.server.database import repository
from src.orchestrate.database_handler import DatabaseHandler

def setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Set up a WebSocket handler
    handler = WebSocketHandler("ws://localhost:8000/ws/flow_run")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set up a database handler and add to the logger
    db_manager = repository.Repository()
    db_handler = DatabaseHandler(db_manager)
    db_formatter = logging.Formatter('%(message)s')
    db_handler.setFormatter(db_formatter)
    logger.addHandler(db_handler)

    return logger, handler

# This code sets up a logger with a WebSocket handler that sends log messages to a specified endpoint. The logger is configured to log messages at the INFO level or higher, and the log messages are formatted with a timestamp, logger name, log level, and the actual message.