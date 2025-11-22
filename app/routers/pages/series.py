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


@router.get('/series', response_class=HTMLResponse, tags=[Tags.page])
def page(request: Request):
    """Render series page"""

    table = get_json_from_api('http://localhost:8000/api/series/all')

    return templates.TemplateResponse(
        request = request, name='series_list.html', context={"table": table}
    )


# @router.get('/series/{series_id}', response_class=HTMLResponse, tags=[Tags.page])
# def details(request: Request, series_id: str):
#     """Render series details page"""

#     series_books = get_json_from_api(f'http://localhost:8000/api/series/books/{series_id}')

#     return templates.TemplateResponse(
#         request = request, name='book_list.html', context={"table": series_books}
#     )



@router.get('/series/details/{series_id}', response_class=HTMLResponse, tags=[Tags.page])
def details(request: Request, series_id: str):
    """Render series details page"""

    series_books = get_json_from_api(f'http://localhost:8000/api/series/details/{series_id}')

    return templates.TemplateResponse(
        request = request, name='series_details.html', context={"table": series_books}
    )