from pydantic import BaseModel, Field


class AuthorQuery(BaseModel):
    author_name: str = Field(
        default=None, title="Author's name", max_length=50, example="pirateaba"
    )


class AuthorResponse(BaseModel):
    id: str
    name: str | None
    authorAsin: str | None
