from fastapi import BackgroundTasks, Query, Form
from typing import Annotated, List
from pydantic import BaseModel

from app.routers.api import api_router
from app.custom_objects import settings
from app.routers.route_tags import Tags
from app.db_models import db_helpers
from app.response_models.serieswatchlist_response import SeriesWatchListResponse
from app.db_models.tables.serieswatchlist import deleteSeriesWatchListItem, getSeriesWatchListItem, getAllSeriesWatchListItems, addSeriesWatchListItem


router = api_router.initRouter()

# Load settings
settings = settings.readSettings()

# init db connection
engine = db_helpers.connectToDb()




@router.get("/user/serieswatchlist", tags=[Tags.user], response_model=List[SeriesWatchListResponse])
async def get_series_watch_list_items():
    """Returns list of all SeriesWatchListItems"""
    results = getAllSeriesWatchListItems(engine)
    if results:
        return results
    return []


@router.get("/user/serieswatchlistitem/{item_id}", tags=[Tags.user], response_model=SeriesWatchListResponse)
async def get_series_watch_list_item():
    """Returns list of all SeriesWatchListItems"""
    results = getSeriesWatchListItem(engine)
    if results:
        return results
    return []


class SeriesWachListModel(BaseModel):
    series_id: str
    model_config = {"extra": "forbid"}

@router.post("/user/addserieswatchlistitem/{item}", tags=[Tags.user])
async def add_watch_list_item(data: Annotated[SeriesWachListModel, Form()]):
    """Add item to the watchlist"""

    if not getSeriesWatchListItem(engine, data.series_id):
        addSeriesWatchListItem(engine, data.series_id)
        return {"message": "Added to watch list"}