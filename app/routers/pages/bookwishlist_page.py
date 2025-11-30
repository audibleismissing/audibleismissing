import json

from os.path import dirname, join
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db_models.views.booksandseries import getViewBookDetails
from app.routers.route_tags import Tags
from app.routers.pages import app_router
from app.routers.api.user_api import get_book_wish_list_items
from app.db_models import db_helpers
from app.custom_objects.settings import readSettings


router = app_router.initRouter()

current_dir = dirname(__file__)
templates_dir = join(current_dir, "../../templates")
templates = Jinja2Templates(directory=templates_dir)

# init db connection
engine = db_helpers.connectToDb()

# Load settings
config = readSettings()


@router.get("/user/bookwishlist/", response_class=HTMLResponse, tags=[Tags.page])
async def page(request: Request):
    """Render book wishlist page"""

    wishlist_items = await get_book_wish_list_items()

    if wishlist_items:
        wishlist_table = []
        for item in wishlist_items:
            single_book = getViewBookDetails(config.sqlite_path, item.bookId)
            wishlist_table.append(single_book)
    else:
        wishlist_table = []

    return templates.TemplateResponse(
        request=request,
        name="book_wish_list.html",
        context={"wishlist_table": wishlist_table},
    )
