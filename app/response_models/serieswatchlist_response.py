from pydantic import BaseModel, Field


class SeriesWatchListQuery(BaseModel):
    watch_list_item_id: str = Field(
        default=None,
        name="Watch list item id",
        max_length=50,
        example="27e7d3a3-3eab-457a-99d0-6973c6ff6ee8"
    )


class SeriesWatchListResponse(BaseModel):
    id: str
    seriesId: str | None