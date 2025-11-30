from typing import List

from pydantic import BaseModel, Field

from .author_response import AuthorResponse
from .genre_response import GenreResponse
from .narrator_response import NarratorResponse
from .series_response import SeriesResponse


class BookQuery(BaseModel):
    book_asin: str = Field(
        default=None, title="Book ASIN", max_length=50, example="1774240327"
    )


class BookResponse(BaseModel):
    id: str
    title: str | None
    subtitle: str | None
    authors: List[AuthorResponse] | None
    publisher: str | None
    copyright: str | None
    description: str | None
    summary: str | None
    isbn: str | None
    bookAsin: str | None
    region: str | None
    language: str | None
    isExplicit: bool | None
    isAbridged: bool | None
    releaseDate: str | None
    genres: List[GenreResponse] | None
    link: str | None
    imageUrl: str | None
    series: List[SeriesResponse] | None
    isOwned: bool | None
    audibleOverallAvgRating: float | None
    audiblePerformanceAvgRating: float | None
    audibleStoryAvgRating: float | None
    narrators: List[NarratorResponse] | None
    lengthMinutes: int | None
    isAudiobook: bool | None
