import websockets
import asyncio
import logging
import json

# WebSocket Logger and Status Handler
class WebSocketHandler(logging.Handler):
    def __init__(self, uri="ws://localhost:8000/ws/flow_run"):
        super().__init__()
        self.uri = uri
        self.loop = asyncio.get_event_loop()        
    
    async def send_status(self, status):
        message = json.dumps({"type": "status", "status": status})
        await self.send_message(message)

    async def send_message(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)

    def emit(self, record):
        log_entry = self.format(record)
        message = json.dumps({"type": "log", "message": log_entry})
        self.loop.run_until_complete(self.send_message(message))