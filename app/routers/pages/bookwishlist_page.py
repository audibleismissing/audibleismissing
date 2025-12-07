import json

from os.path import dirname, join
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db_models.views.booksandseries import getViewBookDetails
from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api.user_api import get_book_wish_list_items
from app.db_models import db_helpers
from app.custom_objects.settings import readSettings


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




@router.get("/user/bookwishlist/", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request, service: SQLiteService = Depends(get_db_service)):
    """Render book wishlist page"""

    wishlist_items = await get_book_wish_list_items(service)

    if wishlist_items:
        wishlist_table = []
        for item in wishlist_items:
            single_book = getViewBookDetails(item.bookId, service)
            wishlist_table.append(single_book)
    else:
        wishlist_table = []

    return templates.TemplateResponse(
        request=request,
        name="book_wish_list.html",
        context={"wishlist_table": wishlist_table},
    )
