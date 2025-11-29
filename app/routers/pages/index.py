import json
from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api import user_api
from app.routers.api import book_api


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, '../../templates')
templates = Jinja2Templates(directory=templates_dir)


@router.get('/', response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request):
    """Render index page"""

    # calendar
    limit = 10
    releases = await book_api.get_book_release_dates(limit)
    watchlist_releases = await user_api.get_book_release_dates(limit)

    return templates.TemplateResponse(
        request = request, name='index.html', context={"releases": releases, "watchlist_releases": watchlist_releases}
    )
