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
    seriesName: str | None
    seriesAsin: str | None
    totalBooksInSeries: int | None
    totalBooksInLibrary: int | None