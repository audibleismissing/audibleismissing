from fastapi import BackgroundTasks, Query, Form
from typing import Annotated, List
from pydantic import BaseModel

from app.routers.api import api_router
from app.custom_objects import settings
from app.routers.route_tags import Tags
from app.db_models import db_helpers
from app.response_models.serieswatchlist_response import SeriesWatchListResponse
from app.response_models.bookwishlist_response import BookWishListResponse
from app.db_models.tables.serieswatchlist import deleteSeriesWatchListItem, getSeriesWatchListItem, getAllSeriesWatchListItems, addSeriesWatchListItem
from app.db_models.tables.bookwishlist import deleteBookWishListItem, getAllBookWishListItems, getBookWishListItem, addBookWishListItem

router = api_router.initRouter()

# Load settings
settings = settings.readSettings()

# init db connection
engine = db_helpers.connectToDb()


# Series watch list
@router.get("/user/serieswatchlist", tags=[Tags.user], response_model=List[SeriesWatchListResponse])
async def get_series_watch_list_items():
    """Returns list of all SeriesWatchListItems"""
    results = getAllSeriesWatchListItems(engine)
    if results:
        return results
    return []


@router.get("/user/serieswatchlistitem/{item_id}", tags=[Tags.user], response_model=SeriesWatchListResponse)
async def get_series_watch_list_item():
    """Returns list of all SeriesWatchListItems"""
    results = getSeriesWatchListItem(engine)
    if results:
        return results
    return {}

class SeriesWatchListModel(BaseModel):
    series_id: str
    model_config = {"extra": "forbid"}

@router.post("/user/addserieswatchlistitem", tags=[Tags.user])
async def add_watch_list_item(data: Annotated[SeriesWatchListModel, Form()]):
    """Add item to the watchlist"""
    item = getSeriesWatchListItem(engine, data.series_id)
    
    if not item:
        addSeriesWatchListItem(engine, data.series_id)
        return {"message": "Added to watch list"}
    return {"message": "Couldn't add to watch list"}


@router.delete("/user/removeserieswatchlistitem/{series_id}", tags=[Tags.user])
async def remove_watch_list_item(series_id: str):
    """Remove item from the watchlist"""
    item = getSeriesWatchListItem(engine, series_id)
    
    if item:
        deleteSeriesWatchListItem(engine, item.id)
        return {"message": "Removed from watch list"}
    return {"message": "Item not in watch list"}
# End Series watch list


# Book wish list
@router.get("/user/bookwishlist", tags=[Tags.user], response_model=List[BookWishListResponse])
async def get_book_wish_list_items():
    """Returns list of all SeriesWatchListItems"""
    results = getAllBookWishListItems(engine)
    if results:
        return results
    return []


@router.get("/user/bookwishlistitem/{item_id}", tags=[Tags.user], response_model=BookWishListResponse)
async def get_book_wish_list_item():
    """Returns list of all SeriesWatchListItems"""
    results = getBookWishListItem(engine)
    if results:
        return results
    return {}

class BookWishListModel(BaseModel):
    book_id: str
    model_config = {"extra": "forbid"}

@router.post("/user/addbookwishlistitem", tags=[Tags.user])
async def add_book_wish_list_item(data: Annotated[BookWishListModel, Form()]):
    """Add item to the wish list"""
    item = getBookWishListItem(engine, data.book_id)

    if not item:
        addBookWishListItem(engine, data.book_id)
        return {"message": "Added to wish list"}
    return {"message": "Couldn't add to wish list"}


@router.delete("/user/removebookwishlistitem/{book_id}", tags=[Tags.user])
async def remove_book_wish_list_item(book_id: str):
    """Remove item from the wish list"""
    item = getBookWishListItem(engine, book_id)

    if item:
        deleteBookWishListItem(engine, item.id)
        return {"message": "Removed from wish list"}
    return {"message": "Item not in wish list"}
# End book wish list