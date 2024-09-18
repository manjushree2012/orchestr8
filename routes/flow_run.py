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

@router.get('/flows/{flow_id}', name='flow_details')
async def flow_details(request: Request, flow_id: str):
    db_manager = Repository()
    flow, flow_runs = db_manager.get_flow_with_runs(flow_id)

    return templates.TemplateResponse(
        request=request,
        name="flow_details.html",
        context = {"flow" : flow, 'flow_runs' : flow_runs }
    )

@router.get('/flow-runs/{flow_run_id}', name='flow_run_details')
async def flow_run_details(request: Request, flow_run_id: str):
    db_manager = Repository()
    flow_run = db_manager.get_flow_run(flow_run_id)

    return templates.TemplateResponse(
        request=request,
        name="flow-run.html",
        context = {'flow_run' : flow_run }
    )

@router.get("/flow-runs", response_class=HTMLResponse, name="flow_runs")
async def flow_runs(request: Request):

    db_manager = Repository()
    flow_runs = db_manager.get_last_N_flow_runs(30)

    return templates.TemplateResponse(
        request=request,
        name="flow-runs.html",
        context = {"flow_runs" : flow_runs}
    )