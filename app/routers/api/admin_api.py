from fastapi import BackgroundTasks, Depends

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.custom_objects import settings
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import (
    taskRefreshAbsData,
    getMissingAudibleBooks,
    refreshAudnexusData,
)
from app.app_helpers.audibleapi.audibleapi_api import loadExistingAuth
from app.services.sqlite import SQLiteService


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()


# init db connection
engine = db_helpers.connectToDb()


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    return SQLiteService()


@router.get("/database/refreshabsdata", tags=[Tags.admin])
async def refresh_abs_Data(background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)):
    """Wipes all data from db and re-import abs data"""
    background_task.add_task(taskRefreshAbsData, engine, settings, service)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/resetdb", tags=[Tags.admin])
async def reset_db(background_task: BackgroundTasks):
    """Drops db and recreates tables"""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/backfill_audible", tags=[Tags.admin])
async def backfill_audible(background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)):
    """Gets missing info from audible. Run /abs/resetdb endpoint first"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        # background_task.add_task(refreshAudibleData, engine, auth)
        # background_task.add_task(refreshAudimetaData, service) # testing audimeta
        background_task.add_task(refreshAudnexusData, service)  # testing audnexus
        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}


@router.get("/database/get_missing_books", tags=[Tags.admin])
async def get_missingBooks(background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)):
    """Gets missing books from audible."""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        background_task.add_task(getMissingAudibleBooks, auth, service)
        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}


@router.get("/database/import", tags=[Tags.admin])
async def import_test_data(background_task: BackgroundTasks):
    """Imports the db from a json file. destructive."""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    background_task.add_task(db_helpers.importJsonToDb, engine)
    return {"message": "Importing data."}


@router.get("/database/export", tags=[Tags.admin])
async def export_test_data(background_task: BackgroundTasks):
    """Exports the db to a json file"""
    background_task.add_task(db_helpers.exportDbToJson, engine)
    return {"message": "Exporting data."}
