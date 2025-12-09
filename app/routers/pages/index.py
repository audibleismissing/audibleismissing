import json
from os.path import dirname, join
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api import user_api
from app.routers.api import book_api

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


@router.get("/", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request, service: SQLiteService = Depends(get_db_service)):
    """Render index page"""

    # calendar
    limit = 10
    releases = await book_api.get_book_release_dates(limit, service)
    watchlist_releases = await user_api.get_book_release_dates(limit, service)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"releases": releases, "watchlist_releases": watchlist_releases},
    )
