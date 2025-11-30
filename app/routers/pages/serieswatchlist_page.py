import json

from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db_models.views.seriesandcounts import getViewSeriesCountsSingleSeries
from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.db_models import db_helpers
from app.custom_objects.settings import readSettings
from app.routers.api.user_api import get_series_watch_list_items


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, "../../templates")
templates = Jinja2Templates(directory=templates_dir)

# init db connection
engine = db_helpers.connectToDb()

# Load settings
config = readSettings()


@router.get("/user/serieswatchlist/", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request):
    """Render series watchlist page"""

    watchlist_items = await get_series_watch_list_items()

    if watchlist_items:
        watchlist_table = []
        for item in watchlist_items:
            single_series = getViewSeriesCountsSingleSeries(
                config.sqlite_path, item.seriesId
            )
            watchlist_table.append(single_series)
    else:
        watchlist_table = []

    return templates.TemplateResponse(
        request=request,
        name="series_watch_list.html",
        context={"watchlist_table": watchlist_table},
    )
