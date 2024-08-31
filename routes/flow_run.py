from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.repository import Repository

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/flow-run", response_class=HTMLResponse)
async def flow_run(request: Request):
    return templates.TemplateResponse(
        request=request, name="flow-run.html"
    )

@router.get("/flows", response_class=HTMLResponse)
async def flows(request: Request):

    db_manager = Repository()
    flows = db_manager.get_all_flows()

    return templates.TemplateResponse(
        request=request, 
        name="flows.html",
        context = {"flows" : flows}
    )