from os.path import dirname, join
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api.series_api import (
    get_series_counts,
    get_series_details,
    get_all_series,
)

from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

# setup global services
db_service = None
background_manager = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service

def get_background_manager() -> BackgroundTaskManagerService:
    """Get the background task manager instance."""
    global background_manager
    if background_manager is None:
        background_manager = BackgroundTaskManagerService()
    return background_manager


# service: SQLiteService = Depends(get_db_service)):

router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, "../../templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/series", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request, service: SQLiteService = Depends(get_db_service)):
    """Render series page"""
    table = await get_all_series(service)

    return templates.TemplateResponse(
        request=request, name="series_list.html", context={"table": table}
    )


@router.get(
    "/series/details/{series_id}", response_class=HTMLResponse, tags=[Tags.page]
)
async def details(request: Request, series_id: str):
    """Render series details page"""
    counts = await get_series_counts(series_id)
    table = await get_series_details(series_id)

    return templates.TemplateResponse(
        request=request,
        name="series_details.html",
        context={"table": table, "counts": counts},
    )
