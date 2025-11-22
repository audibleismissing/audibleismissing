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


@router.get('/books', response_class=HTMLResponse, tags=[Tags.page])
def page(request: Request):
    """Render books page"""

    table = get_json_from_api('http://localhost:8000/api/books/all')

    return templates.TemplateResponse(
        request = request, name='book_list.html', context={"table": table}
    )
