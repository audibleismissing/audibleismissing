from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api.book_api import get_all_books, get_book_authors, get_book_details, get_book_genres, get_book_narrators


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, '../../templates')
templates = Jinja2Templates(directory=templates_dir)


@router.get('/books', response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request):
    """Render books page"""

    table = await get_all_books()

    return templates.TemplateResponse(
        request = request, name='book_list.html', context={"table": table}
    )


@router.get('/book/details/{book_id}', response_class=HTMLResponse, tags=[Tags.page])
async def details(request: Request, book_id: str):
    """Render book details page"""
    details = await get_book_details(book_id)
    authors = await get_book_authors(book_id)
    narrators = await get_book_narrators(book_id)
    genres = await get_book_genres(book_id)

    return templates.TemplateResponse(
        request = request, name='book_details.html', context={"details": details, "authors": authors, "narrators": narrators, "genres": genres}
    )
