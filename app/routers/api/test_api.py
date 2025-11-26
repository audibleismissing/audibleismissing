from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router, book_api
from app.routers.route_tags import Tags
from app.response_models import book_response, series_response, series_view
from app.custom_objects import settings
from app.app_helpers.audiobookshelf import abs_helpers
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData
from app.app_helpers.audibleapi.api import getAudibleBooksInSeries, getAudibleBook
from app.app_helpers.audibleapi.auth import loadExistingAuth

from app.db_models.tables import series as series_table
from app.db_models.views import booksandseries, seriesandcounts


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()


# init db connection
engine = db_helpers.connectToDb()



@router.get("/test/importtestdatajson", tags=[Tags.test])
async def import_test_data(background_task: BackgroundTasks):
    """Wipes all data from db and re-import abs data"""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    background_task.add_task(db_helpers.importDb, engine)
    return {"message": "Refreshing data. This may take a while."}


@router.get('/test/getAudibleBook/{book_asin}', tags=[Tags.test])
async def test_getAudibleBook(book_asin: str):
    """Get list of books in a series by series id"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        results = getAudibleBook(auth, book_asin)
        if results:
            return results
        return []
    return {"message": "Audible auth error."}


@router.get('/test/getAudibleBooksInSeries/{book_asin}', tags=[Tags.test])
async def test_getAudibleBooksInSeries(book_asin: str):
    """Get list of books in a series by series id"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        results = getAudibleBooksInSeries(auth, book_asin)
        if results:
            return results
        return []
    return {"message": "Audible auth error."}