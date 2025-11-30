from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import book_response, series_response, series_view
from app.custom_objects import settings
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData

from app.db_models.tables import series as series_table
from app.db_models.views import booksandseries, seriesandcounts


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()


# init db connection
engine = db_helpers.connectToDb()


# /api/series/all/
# getAllSeries -> [Series]

@router.get("/series/all", tags=[Tags.series], response_model=List[series_view.SeriesViewResponse])
async def get_all_series():
    """Returns list of all series"""
    results = seriesandcounts.getViewSeriesCounts(settings.sqlite_path)

    if results:
        return results
    return []


@router.get('/series/books/{series_id}', tags=[Tags.series], response_model=List[book_response.BookResponse])
async def get_series_by_series_id(series_id: str):
    """Get list of books in a series by series id"""
    results = series_table.getBooksInSeries(engine, series_id)
    if results:
        return results
    return []


@router.get('/series/details/{series_id}', tags=[Tags.series])
async def get_series_details(series_id: str):
    """Get series details from view."""
    results = booksandseries.getViewSeriesDetails(settings.sqlite_path, series_id)
    if results:
        return results
    return []


@router.get('/series/counts/{series_id}', tags=[Tags.series])
async def get_series_counts(series_id: str):
    """Get series counts from view."""
    results = seriesandcounts.getViewSeriesCountsBySeries(settings.sqlite_path, series_id)
    if results:
        return results
    return []