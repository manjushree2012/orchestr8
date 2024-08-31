from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import index
from . import flow_run
from . import websocket

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Serve static files from the `static` directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(index.router)
app.include_router(flow_run.router)
app.include_router(websocket.router)