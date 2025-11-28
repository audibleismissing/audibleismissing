from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.app_helpers.rest_handler.methods import get_json_from_api


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, '../../templates')
templates = Jinja2Templates(directory=templates_dir)


@router.get('/user/serieswatchlist/', response_class=HTMLResponse, tags=[Tags.page])
def page(request: Request):
    """Render series watchlist page"""

    watchlist_table = get_json_from_api('http://localhost:8000/api/user/serieswatchlist')

    return templates.TemplateResponse(
        request = request, name='series_watch_list.html', context={"watchlist_table": watchlist_table}
    )
