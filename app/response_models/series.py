from pydantic import BaseModel, Field


class SeriesQuery(BaseModel):
    author_name: str = Field(
        default=None,
        name="Series' name",
        max_length=50,
        example="The Wandering Inn"
    )


class SeriesResponse(BaseModel):
    id: str
    name: str | None
    seriesAsin: str | None
    sequence: str | None
    totalBooksInSeries: int | None