from fastapi import BackgroundTasks

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.custom_objects import settings
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData, refreshAudibleData, refreshAudnexusData, refreshAudimetaData
from app.app_helpers.audibleapi.auth import loadExistingAuth


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()


# init db connection
engine = db_helpers.connectToDb()


@router.get("/database/refreshabsdata", tags=[Tags.admin])
async def refresh_abs_Data(background_task: BackgroundTasks):
    """Wipes all data from db and re-import abs data"""
    background_task.add_task(taskRefreshAbsData, engine, settings)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/resetdb", tags=[Tags.admin])
async def reset_db(background_task: BackgroundTasks):
    """Drops db and recreates tables"""
    db_helpers.resetAllData(engine, settings.sqlite_path)
    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/backfill_audible", tags=[Tags.admin])
async def backfill_audible(background_task: BackgroundTasks):
    """Gets missing info from audible. Run /abs/resetdb endpoint first"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        # background_task.add_task(refreshAudibleData, engine, auth)
        # background_task.add_task(refreshAudimetaData, engine) # testing audimeta
        background_task.add_task(refreshAudnexusData, engine) # testing audnexus
        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}


@router.get("/database/get_missing_books", tags=[Tags.admin])
async def get_missingBooks(background_task: BackgroundTasks):
    """Gets missing info from audible. Run /abs/resetdb endpoint first"""
    auth = loadExistingAuth(settings.audible_auth)
    if auth:
        background_task.add_task(refreshAudibleData, engine, auth)
        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}

