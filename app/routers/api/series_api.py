from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import series, book
from app.custom_objects import settings
from app.app_helpers.audiobookshelf import abs_helpers
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData

from app.db_models.tables import series as series_table
from app.db_models.views import booksandseries


router = api_router.initRouter()


# Load settings from settings.toml
# file = "/src/audibleismissing/settings.toml"
file = "settings.toml"
settings = settings.readSettings(file)


# init db connection
engine = db_helpers.connectToDb()


# /api/series/all/
# getAllSeries -> [Series]

@router.get("/series/all", tags=[Tags.series], response_model=List[series.SeriesResponse])
async def get_all_series():
    """Returns list of all series"""
    results = series_table.getAllSeries(engine)
    return results


@router.get('/series/books/{series_id}', tags=[Tags.series], response_model=List[book.BookResponse])
async def get_series_by_series_id(series_id: str):
    """Get list of books in a series by series id"""
    results = series_table.getBooksInSeries(engine, series_id)
    return results


@router.get('/series/details/{series_id}', tags=[Tags.series])
async def get_series_details(series_id: str):
    """Get series details from view."""
    results = booksandseries.getViewSeriesDetails(settings.sqlite_path, series_id)
    return results
