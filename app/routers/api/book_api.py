from fastapi import BackgroundTasks, Query
from typing import Annotated, List

from app.routers.api import api_router
from app.routers.route_tags import Tags
from app.response_models import book
from app.custom_objects import settings
from app.app_helpers.audiobookshelf import abs_helpers
from app.db_models import db_helpers
from app.app_helpers.fastapi_utils.fastapi_tasks import taskRefreshAbsData

from app.db_models.tables import books as books_table
from app.db_models.tables import series as series_table
from app.db_models.views import booksandseries



router = api_router.initRouter()


# Load settings from settings.toml
# file = "/src/audibleismissing/settings.toml"
file = "settings.toml"
settings = settings.readSettings(file)


# init db connection
engine = db_helpers.connectToDb()


@router.get("/books/all", tags=[Tags.book], response_model=List[book.BookResponse])
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


@router.get("/book/{book_asin}", tags=[Tags.book], response_model=book.BookResponse)
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


@router.get("/book/releasedates/{limit}", tags=[Tags.book])#, response_model=List[book.BookResponse])
async def get_book_release_dates(limit: int):
    """Gets books to be released. results limit."""
    # results = books_table.getBooksToBeReleased(engine, limit)
    results = booksandseries.getViewReleaseDates(settings.sqlite_path, limit)

    if results:
        return results
    return []


# @router.get("/book/series/{search_string}", tags=[Tags.book], response_model=List[book.BookResponse])
# async def get_books_in_series(search_string: str):
#     """Returns list of all books in a series with given book asin or title"""
#     results = series_table.getSeriesByBookAsin(engine, search_string)
#     return results
# # FIX: getSeriesByBookAsin is missing


# @router.get("/book/author/{author_name}", tags=[Tags.book], response_model=List[book.BookResponse])
# async def get_books_by_author(author_name: str):
#     """Returns list of all books by a given authors name"""
#     return {"message": "Not implemented yet"}
