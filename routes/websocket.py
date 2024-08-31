from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

@router.websocket("/ws/flow_run")
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

# @router.websocket("/ws/{flow_run_id}")
# async def websocket_endpoint(websocket: WebSocket, flow_run_id: str):
#     await websocket.accept()
#     try:
#         last_status = None  # Keep track of the last sent status
#         while True:
#             # Simulate status changes
#             current_status = flow_status_store.get(flow_run_id, 'PENDING')
#             await websocket.send_text(current_status)

#             await asyncio.sleep(4)

#             await websocket.send_text('RUNNING')
#             await asyncio.sleep(4)
#             await websocket.send_text('COMPLETED')

#             break
        
#             # Send the status only if it has changed
#             if current_status != last_status:
#                 await websocket.send_text(current_status)
#                 last_status = current_status

#             # If the flow is completed or errored, close the connection
#             if current_status in ['COMPLETED', 'ERROR']:
#                 break

#             await asyncio.sleep(1)  # Adjust the polling interval as needed
#     except WebSocketDisconnect:
#         print(f"WebSocket disconnected for flow {flow_run_id}")
#     finally:
#         await websocket.close()