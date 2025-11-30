from pydantic import BaseModel, Field


class BookWishListQuery(BaseModel):
    watch_list_item_id: str = Field(
        default=None,
        name="Wish list item id",
        max_length=50,
        example="27e7d3a3-3eab-457a-99d0-6973c6ff6ee8",
    )


class BookWishListResponse(BaseModel):
    id: str
    bookId: str | None
