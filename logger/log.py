import logging
from websocket_handler import WebSocketHandler

def setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Set up a WebSocket handler
    handler = WebSocketHandler("ws://localhost:8000/ws/flow_run")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, handler

# This code sets up a logger with a WebSocket handler that sends log messages to a specified endpoint. The logger is configured to log messages at the INFO level or higher, and the log messages are formatted with a timestamp, logger name, log level, and the actual message.