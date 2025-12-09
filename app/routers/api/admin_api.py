from fastapi import BackgroundTasks, Depends

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.custom_objects import settings
from app.app_helpers.audibleapi.audibleapi_api import loadExistingAuth


from app.services import task_manager
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


# service: SQLiteService = Depends(get_db_service)


router = api_router.initRouter()


settings = settings.readSettings()


@router.get("/database/refreshabsdata", tags=[Tags.admin])
async def refresh_abs_Data(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Import abs data"""
    # background_task.add_task(taskRefreshAbsData, settings, service)
    job_manager = get_background_manager()
    await job_manager.job_refresh_audiobookshelf_data()

    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/resetdb", tags=[Tags.admin])
async def reset_db(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Drops db and recreates tables"""
    service.dropAllTables()
    service.create_tables()
    return {"message": "Refreshing data. This may take a while."}


@router.get("/database/backfill_audible", tags=[Tags.admin])
async def backfill_audible(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Gets missing info from audible. Run /abs/resetdb endpoint first"""
    # auth = loadExistingAuth(settings.audible_auth_file)
    # if auth:

    job_manager = get_background_manager()
    await job_manager.job_refresh_book_metadata()

    return {"message": "Refreshing data. This may take a while."}
    # return {"message": "Not authenticated to audible."}


@router.get("/database/get_missing_books", tags=[Tags.admin])
async def get_missingBooks(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Gets missing books from audible."""
    auth = loadExistingAuth()

    if auth:
        job_manager = get_background_manager()
        await job_manager.job_check_for_new_books()

        return {"message": "Refreshing data. This may take a while."}
    return {"message": "Not authenticated to audible."}


@router.get("/database/import", tags=[Tags.admin])
async def import_test_data(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Imports the db from a json file. destructive."""
    service.dropAllTables()
    service.create_tables()

    background_task.add_task(service.importJsonToDb)
    return {"message": "Importing data."}


@router.get("/database/export", tags=[Tags.admin])
async def export_test_data(
    background_task: BackgroundTasks, service: SQLiteService = Depends(get_db_service)
):
    """Exports the db to a json file"""
    background_task.add_task(service.exportDbToJson)
    return {"message": "Exporting data."}
