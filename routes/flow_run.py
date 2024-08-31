from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/flow-run", response_class=HTMLResponse)
async def flow_run(request: Request):
    return templates.TemplateResponse(
        request=request, name="flow-run.html"
    )