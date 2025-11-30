from app.app_helpers.audiobookshelf.audiobookshelf_functions import refreshAbsData
from app.db_models import db_helpers
from app.app_helpers.audibleapi import audibleapi_functions as audible_functions

# testing audimeta - doesn't want to return series data
from app.app_helpers.audimeta import audimeta_functions
# testing audnexus
from app.app_helpers.audnexus import audnexus_functions



def taskRefreshAbsData(engine, settings):
    """refresh all data in database from audiobookshelf"""
    print("Starting taskRefreshAbsData")
    refreshAbsData(engine, settings.abs_url, settings.abs_api_key, settings.abs_library_id)
    print("Completed taskRefreshAbsData")


def getMissingAudibleBooks(engine, auth):
    print("Starting getMissingAudibleBooks")
    audible_functions.getMissingBooks(engine, auth)
    print("Completed getMissingAudibleBooks")


# testing audnexus
def refreshAudnexusData(engine):
    print("Starting backfillAudnexusBookData")
    audnexus_functions.backfillAudnexusBookData(engine)
    print("Completed backfillAudnexusBookData")


# def refreshAudimetaData(engine):
#     print("Starting getMissingBooks")
#     audimeta_functions.getMissingBooks(engine)
#     print("Completed getMissingBooks")
    