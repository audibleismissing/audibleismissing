from fastapi import Query, Depends
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import book_response, series_response, series_view

from app.db_models.tables import series as series_table
from app.db_models.views import booksandseries, seriesandcounts


from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

# setup global services
database = None
background_manager = None


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global database
    if database is None:
        database = SQLiteService()
    return database


def get_background_manager() -> BackgroundTaskManagerService:
    """Get the background task manager instance."""
    global background_manager
    if background_manager is None:
        background_manager = BackgroundTaskManagerService()
    return background_manager


# service: SQLiteService = Depends(get_db_service)):

router = api_router.initRouter()


@router.get(
    "/series/all",
    tags=[Tags.series],
    response_model=List[series_view.SeriesViewResponse],
)
async def get_all_series(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all series"""
    results = seriesandcounts.getViewSeriesCounts(service)

    if results:
        return results
    return []


@router.get(
    "/series/books/{series_id}",
    tags=[Tags.series],
    response_model=List[book_response.BookResponse],
)
async def get_series_by_series_id(
    series_id: str, service: SQLiteService = Depends(get_db_service)
):
    """Get list of books in a series by series id"""
    results = series_table.getBooksInSeries(series_id, service)
    if results:
        return results
    return []


@router.get("/series/details/{series_id}", tags=[Tags.series])
async def get_series_details(
    series_id: str, service: SQLiteService = Depends(get_db_service)
):
    """Get series details from view."""
    results = booksandseries.getViewSeriesDetails(series_id, service)
    if results:
        return results
    return []


@router.get("/series/counts/{series_id}", tags=[Tags.series])
async def get_series_counts(
    series_id: str, service: SQLiteService = Depends(get_db_service)
):
    """Get series counts from view."""
    results = seriesandcounts.getViewSeriesCountsBySeries(series_id, service)
    if results:
        return results
    return []
