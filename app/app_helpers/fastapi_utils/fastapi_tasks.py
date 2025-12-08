# from app.app_helpers.audiobookshelf.audiobookshelf_functions import refreshAbsData
# from app.db_models import db_helpers
# from app.app_helpers.audibleapi import audibleapi_functions as audible_functions

# from fastapi import Depends

# # testing audimeta - doesn't want to return series data
# from app.app_helpers.audimeta import audimeta_functions

# # testing audnexus
# from app.app_helpers.audnexus import audnexus_functions


# from app.services.sqlite import SQLiteService
# from app.services.task_manager import BackgroundTaskManagerService


# # setup global services
# db_service = None
# background_manager = None

# def get_db_service() -> SQLiteService:
#     """Get the database service instance."""
#     global db_service
#     if db_service is None:
#         db_service = SQLiteService()
#     return db_service

# def get_background_manager() -> BackgroundTaskManagerService:
#     """Get the background task manager instance."""
#     global background_manager
#     if background_manager is None:
#         background_manager = BackgroundTaskManagerService()
#     return background_manager


# service: SQLiteService = Depends(get_db_service)



# def taskRefreshAbsData(settings, service: SQLiteService):
#     """refresh all data in database from audiobookshelf"""
#     print("Starting taskRefreshAbsData")
#     refreshAbsData(
#         settings.abs_url, settings.abs_api_key, settings.abs_library_id, service
#     )
#     print("Completed taskRefreshAbsData")


# def getMissingAudibleBooks(auth, service: SQLiteService):
#     print("Starting getMissingAudibleBooks")
#     audible_functions.getMissingBooks(auth, service)
#     print("Completed getMissingAudibleBooks")


# testing audnexus
# def refreshAudnexusData(service: SQLiteService):
#     print("Starting backfillAudnexusBookData")
#     audnexus_functions.backfillAudnexusBookData(service.engine)
#     print("Completed backfillAudnexusBookData")


# def refreshAudimetaData(engine):
#     print("Starting getMissingBooks")
#     audimeta_functions.getMissingBooks(engine)
#     print("Completed getMissingBooks")
