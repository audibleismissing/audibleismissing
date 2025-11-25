from app.app_helpers.audiobookshelf import abs_helpers
from app.db_models import db_helpers
from app.app_helpers.audibleapi.funtions import backfillAudibleData



def taskRefreshAbsData(engine, settings):
    """refresh all data in database from audiobookshelf"""
    print("Starting taskRefreshAbsData")
    db_helpers.resetAllData(engine, settings.sqlite_path)
    abs_helpers.refreshAbsData(engine, settings.abs_url, settings.abs_api_key, settings.abs_library_id)
    print("Completed taskRefreshAbsData")


def refreshAudibleData(engine, auth):
    print("Starting refreshAudibleData")
    backfillAudibleData(engine, auth)
    print("Completed refreshAudibleData")