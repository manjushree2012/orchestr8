from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# import plotly.graph_objects as go

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Serve static files from the `static` directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/old", response_class=HTMLResponse)
async def old_template(request: Request):
    return templates.TemplateResponse(
        request=request, name="_old.html"
    )

@app.get("/flow-run", response_class=HTMLResponse)
async def flow_run(request: Request):
    return templates.TemplateResponse(
        request=request, name="flow-run.html"
    )