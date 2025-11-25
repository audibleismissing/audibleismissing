from pydantic import BaseModel, Field


class NarratorQuery(BaseModel):
    book_asin: str = Field(
        default=None,
        name="Narrator's name",
        max_length=50,
        example="Andrea Parsneau"
    )


class NarratorResponse(BaseModel):
    id: str
    name: str | None