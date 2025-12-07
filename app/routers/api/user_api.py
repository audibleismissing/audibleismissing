from fastapi import BackgroundTasks, Query, Form, Depends
from typing import Annotated, List
from pydantic import BaseModel

from app.routers.api import api_router
from app.custom_objects import settings
from app.routers.route_tags import Tags

from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

from app.response_models.serieswatchlist_response import SeriesWatchListResponse
from app.response_models.bookwishlist_response import BookWishListResponse
from app.db_models.tables.serieswatchlist import (
    deleteSeriesWatchListItem,
    getSeriesWatchListItem,
    getAllSeriesWatchListItems,
    addSeriesWatchListItem,
)
from app.db_models.tables.bookwishlist import (
    deleteBookWishListItem,
    getAllBookWishListItems,
    getBookWishListItem,
    addBookWishListItem,
)
from app.db_models.views import booksandseries

router = api_router.initRouter()




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



# Series watch list
@router.get(
    "/user/serieswatchlist",
    tags=[Tags.user],
    response_model=List[SeriesWatchListResponse],
)
async def get_series_watch_list_items(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all SeriesWatchListItems"""
    results = getAllSeriesWatchListItems(service)
    if results:
        return results
    return []


@router.get("/user/serieswatchlist/releasedates/{limit}", tags=[Tags.user])
async def get_book_release_dates(limit: int, service: SQLiteService = Depends(get_db_service)):
    """Gets books to be released on wachlist. results limit."""
    results = booksandseries.getViewWatchListReleaseDates(limit, service)

    if results:
        return results
    return []


@router.get(
    "/user/serieswatchlistitem/{item_id}",
    tags=[Tags.user],
    response_model=SeriesWatchListResponse,
)
async def get_series_watch_list_item(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all SeriesWatchListItems"""
    results = getSeriesWatchListItem(service)
    if results:
        return results
    return {}


class SeriesWatchListModel(BaseModel):
    series_id: str
    model_config = {"extra": "forbid"}


@router.post("/user/addserieswatchlistitem", tags=[Tags.user])
async def add_watch_list_item(data: Annotated[SeriesWatchListModel, Form()], service: SQLiteService = Depends(get_db_service)):
    """Add item to the watchlist"""
    item = getSeriesWatchListItem(service, data.series_id)

    if not item:
        addSeriesWatchListItem(data.series_id, service)
        return {"message": "Added to watch list"}
    return {"message": "Couldn't add to watch list"}


@router.delete("/user/removeserieswatchlistitem/{series_id}", tags=[Tags.user])
async def remove_watch_list_item(series_id: str, service: SQLiteService = Depends(get_db_service)):
    """Remove item from the watchlist"""
    item = getSeriesWatchListItem(service, series_id)

    if item:
        deleteSeriesWatchListItem(item.id, service)
        return {"message": "Removed from watch list"}
    return {"message": "Item not in watch list"}


# End Series watch list


# Book wish list
@router.get(
    "/user/bookwishlist", tags=[Tags.user], response_model=List[BookWishListResponse]
)
async def get_book_wish_list_items(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all SeriesWatchListItems"""
    results = getAllBookWishListItems(service)
    if results:
        return results
    return []


@router.get(
    "/user/bookwishlistitem/{item_id}",
    tags=[Tags.user],
    response_model=BookWishListResponse,
)
async def get_book_wish_list_item(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all SeriesWatchListItems"""
    results = getBookWishListItem(service)
    if results:
        return results
    return {}


class BookWishListModel(BaseModel):
    book_id: str
    model_config = {"extra": "forbid"}


@router.post("/user/addbookwishlistitem", tags=[Tags.user])
async def add_book_wish_list_item(data: Annotated[BookWishListModel, Form()], service: SQLiteService = Depends(get_db_service)):
    """Add item to the wish list"""
    item = getBookWishListItem(service, data.book_id)

    if not item:
        addBookWishListItem(data.book_id, service)
        return {"message": "Added to wish list"}
    return {"message": "Couldn't add to wish list"}


@router.delete("/user/removebookwishlistitem/{book_id}", tags=[Tags.user])
async def remove_book_wish_list_item(book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Remove item from the wish list"""
    item = getBookWishListItem(service, book_id)

    if item:
        deleteBookWishListItem(item.id, service)
        return {"message": "Removed from wish list"}
    return {"message": "Item not in wish list"}


# End book wish list
