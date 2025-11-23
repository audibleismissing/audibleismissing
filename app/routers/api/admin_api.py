from fastapi import BackgroundTasks

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.custom_objects import settings
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData
from app.app_helpers.audibleapi.funtions import backfillAudibleData
from app.app_helpers.audibleapi.auth import loadExistingAuth
from app.db_models.db_helpers import exportDb, importDb


router = api_router.initRouter()


# Load settings from settings.toml
# file = "/src/audibleismissing/settings.toml"
file = "settings.toml"
settings = settings.readSettings(file)


# init db connection
engine = db_helpers.connectToDb()


@router.get("/abs/refreshabsdata", tags=[Tags.admin])
async def refresh_abs_Data(background_task: BackgroundTasks):
    """Wipes all data from db and re-import abs data"""
    background_task.add_task(taskRefreshAbsData, engine, settings)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/abs/resetdb", tags=[Tags.admin])
async def reset_db(background_task: BackgroundTasks):
    """Drops db and recreates tables"""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/abs/backfill_audible", tags=[Tags.admin])
async def backfill_audible(background_task: BackgroundTasks):
    """Gets missing info from audible. Run /abs/resetdb endpoint first"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        background_task.add_task(backfillAudibleData, engine, auth)
        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}


@router.get("/abs/importtestdatajson", tags=[Tags.admin])
async def import_test_data(background_task: BackgroundTasks):
    """Wipes all data from db and re-import abs data"""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    background_task.add_task(importDb, engine)
    return {"message": "Refreshing data. This may take a while."}


# FIXME: export to json
# @router.get("/abs/exporttestdatajson", tags=[Tags.admin])
# async def export_test_data(background_task: BackgroundTasks):
#     """Exports data to json. Creates a large and small dataset."""
#     background_task.add_task(exportDb, engine)
#     return {"message": "Exporting data. This may take a while."}