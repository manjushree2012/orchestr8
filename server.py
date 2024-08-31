from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Serve static files from the `static` directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/flow-run", response_class=HTMLResponse)
async def flow_run(request: Request):
    return templates.TemplateResponse(
        request=request, name="flow-run.html"
    )
























































class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/flow_run")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Listen for messages from the logger or other sources
            data = await websocket.receive_text()

            # Broadcast the message to all connected clients
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")



from data_store import flow_status_store
import asyncio
@app.websocket("/ws/{flow_run_id}")
async def websocket_endpoint(websocket: WebSocket, flow_run_id: str):
    await websocket.accept()
    try:
        last_status = None  # Keep track of the last sent status
        while True:
            # Simulate status changes
            current_status = flow_status_store.get(flow_run_id, 'PENDING')
            await websocket.send_text(current_status)

            await asyncio.sleep(4)

            await websocket.send_text('RUNNING')
            await asyncio.sleep(4)
            await websocket.send_text('COMPLETED')

            break
        
            # Send the status only if it has changed
            if current_status != last_status:
                await websocket.send_text(current_status)
                last_status = current_status

            # If the flow is completed or errored, close the connection
            if current_status in ['COMPLETED', 'ERROR']:
                break

            await asyncio.sleep(1)  # Adjust the polling interval as needed
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for flow {flow_run_id}")
    finally:
        await websocket.close()