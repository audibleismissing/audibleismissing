from pydantic import BaseModel, Field


class GenreQuery(BaseModel):
    book_asin: str = Field(
        default=None,
        name="Genre name",
        max_length=50,
        example="Fantasy"
    )


class GenreResponse(BaseModel):
    id: str
    name: str | None