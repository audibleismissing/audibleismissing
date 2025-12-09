from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import book_response, series_response, series_view
from app.custom_objects import settings
from app.db_models import db_helpers

from app.db_models.tables import authors as authors_table
from app.db_models.views import booksandseries, seriesandcounts


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()
