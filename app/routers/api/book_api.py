from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import (
    author_response,
    book_response,
    narrator_response,
    genre_response,
)
from app.custom_objects import narrator, settings
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData

from app.db_models.tables import books as books_table
from app.db_models.tables import series as series_table
from app.db_models.tables import authors as authors_table
from app.db_models.tables import narrators as narrators_table
from app.db_models.tables import genres as genres_table
from app.db_models.views import booksandseries


router = api_router.initRouter()


# Load settings
settings = settings.readSettings()


# init db connection
engine = db_helpers.connectToDb()


@router.get(
    "/books/all", tags=[Tags.book], response_model=List[book_response.BookResponse]
)
async def get_all_books():
    """Returns list of all books"""
    results = books_table.getAllBooks(engine)
    if results:
        return results
    return []


@router.get("/books/allview", tags=[Tags.book])
async def get_all_books_view():
    """Returns list of all books from booksandseries view"""
    results = booksandseries.getViewAllBooks(settings.sqlite_path)
    if results:
        return results
    return []


@router.get(
    "/book/{book_asin}", tags=[Tags.book], response_model=book_response.BookResponse
)
async def get_book(book_asin: str):
    """Returns single book by asin"""
    results = books_table.getBook(engine, book_asin)
    if results:
        return results
    return []


@router.get("/book/details/{book_id}", tags=[Tags.book])
async def get_book_details(book_id: str):
    """Returns single book by book id from details view"""
    results = booksandseries.getViewBookDetails(settings.sqlite_path, book_id)
    if results:
        return results
    return {}


@router.get("/book/releasedates/{limit}", tags=[Tags.book])
async def get_book_release_dates(limit: int):
    """Gets books to be released. results limit."""
    results = booksandseries.getViewReleaseDates(settings.sqlite_path, limit)

    if results:
        return results
    return []


@router.get(
    "/book/authors/{book_id}",
    tags=[Tags.book],
    response_model=List[author_response.AuthorResponse],
)
async def get_book_authors(book_id: str):
    """Returns list of authors for a given book id"""
    results = authors_table.getBookAuthors(engine, book_id)
    if results:
        return results
    return []


@router.get(
    "/book/narrators/{book_id}",
    tags=[Tags.book],
    response_model=List[narrator_response.NarratorResponse],
)
async def get_book_narrators(book_id: str):
    """Returns list of narrators for a given book id"""
    results = narrators_table.getBookNarrators(engine, book_id)
    if results:
        return results
    return []


@router.get(
    "/book/genres/{book_id}",
    tags=[Tags.book],
    response_model=List[genre_response.GenreResponse],
)
async def get_book_genres(book_id: str):
    """Returns list of genres for a given book id"""
    results = genres_table.getBookGenres(engine, book_id)
    if results:
        return results
    return []
