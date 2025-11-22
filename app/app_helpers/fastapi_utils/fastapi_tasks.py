from app.app_helpers.audiobookshelf import abs_helpers
from app.db_models import db_helpers
# from functions.audibleapi import backfillAudibleData



def taskRefreshAbsData(engine, settings):
    """refresh all data in database from audiobookshelf"""
    print("Starting taskRefreshAbsData")
    db_helpers.resetAllData(engine, settings.sqlite_path)
    abs_helpers.refreshAbsData(engine, settings.abs_url, settings.abs_api_key, settings.abs_library_id)
    print("Completed taskRefreshAbsData")


# def taskGetMissing(engine, auth):
#     """Get books missing from series and update database"""
#     print("Starting taskGetMissing")
#     backfillAudibleData(engine, auth)
#     print("Completed taskGetMissing")