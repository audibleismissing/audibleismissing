from os.path import dirname, join
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api.book_api import (
    get_all_books,
    get_book_authors,
    get_book_details,
    get_book_genres,
    get_book_narrators,
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


# service: SQLiteService = Depends(get_db_service)



router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, "../../templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/books", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request, service: SQLiteService = Depends(get_db_service)):
    """Render books page"""

    table = await get_all_books(service)

    return templates.TemplateResponse(
        request=request, name="book_list.html", context={"table": table}
    )


@router.get("/book/details/{book_id}", response_class=HTMLResponse, tags=[Tags.page])
async def details(request: Request, book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Render book details page"""
    details = await get_book_details(book_id, service)
    authors = await get_book_authors(book_id, service)
    narrators = await get_book_narrators(book_id, service)
    genres = await get_book_genres(book_id, service)

    return templates.TemplateResponse(
        request=request,
        name="book_details.html",
        context={
            "details": details,
            "authors": authors,
            "narrators": narrators,
            "genres": genres,
        },
    )
