from fastapi import BackgroundTasks, Query, Depends
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



from app.services.sqlite import SQLiteService
from app.services.task_manager import BackgroundTaskManagerService

# setup global services
db_service = None
background_manager = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service

def get_background_manager() -> BackgroundTaskManagerService:
    """Get the background task manager instance."""
    global background_manager
    if background_manager is None:
        background_manager = BackgroundTaskManagerService()
    return background_manager


# service: SQLiteService = Depends(get_db_service)):


router = api_router.initRouter()







@router.get(
    "/books/all", tags=[Tags.book], response_model=List[book_response.BookResponse]
)
async def get_all_books(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all books"""
    results = books_table.getAllBooks(service.engine)
    if results:
        return results
    return []


@router.get("/books/allview", tags=[Tags.book])
async def get_all_books_view(service: SQLiteService = Depends(get_db_service)):
    """Returns list of all books from booksandseries view"""
    results = booksandseries.getViewAllBooks(service.db_path)
    if results:
        return results
    return []


@router.get(
    "/book/{book_asin}", tags=[Tags.book], response_model=book_response.BookResponse
)
async def get_book(book_asin: str, service: SQLiteService = Depends(get_db_service)):
    """Returns single book by asin"""
    results = books_table.getBook(service.engine, book_asin)
    if results:
        return results
    return []


@router.get("/book/details/{book_id}", tags=[Tags.book])
async def get_book_details(book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Returns single book by book id from details view"""
    results = booksandseries.getViewBookDetails(service.db_path, book_id)
    if results:
        return results
    return {}


@router.get("/book/releasedates/{limit}", tags=[Tags.book])
async def get_book_release_dates(limit: int, service: SQLiteService = Depends(get_db_service)):
    """Gets books to be released. results limit."""
    results = booksandseries.getViewReleaseDates(service.db_path, limit)

    if results:
        return results
    return []


@router.get(
    "/book/authors/{book_id}",
    tags=[Tags.book],
    response_model=List[author_response.AuthorResponse],
)
async def get_book_authors(book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Returns list of authors for a given book id"""
    results = authors_table.getBookAuthors(service.engine, book_id)
    if results:
        return results
    return []


@router.get(
    "/book/narrators/{book_id}",
    tags=[Tags.book],
    response_model=List[narrator_response.NarratorResponse],
)
async def get_book_narrators(book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Returns list of narrators for a given book id"""
    results = narrators_table.getBookNarrators(service.engine, book_id)
    if results:
        return results
    return []


@router.get(
    "/book/genres/{book_id}",
    tags=[Tags.book],
    response_model=List[genre_response.GenreResponse],
)
async def get_book_genres(book_id: str, service: SQLiteService = Depends(get_db_service)):
    """Returns list of genres for a given book id"""
    results = genres_table.getBookGenres(service.engine, book_id)
    if results:
        return results
    return []
