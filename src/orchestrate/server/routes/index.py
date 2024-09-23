import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..database.repository import Repository

router = APIRouter()


grandparent_dir = os.path.dirname(os.path.dirname(__file__))
templates_dir = os.path.join(grandparent_dir, 'templates')
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    db_manager = Repository()
    last_30_flows_runs = db_manager.get_last_N_flow_runs(30)
    active_flows = db_manager.get_all_flows()

    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"last_30_flows_runs": last_30_flows_runs, 'active_flows' : active_flows}
    )