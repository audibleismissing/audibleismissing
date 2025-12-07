from app.custom_objects.book import Book

from app.db_models.tables.authors import addAuthor
from app.db_models.tables.authorsmappings import addAuthorMapping
from app.db_models.tables.books import addBook
from app.db_models.tables.genres import addGenre
from app.db_models.tables.genremappings import addGenreMapping
from app.db_models.tables.narrators import addNarrator
from app.db_models.tables.narratormappings import addNarratorMapping
from app.db_models.tables.series import addSeries
from app.db_models.tables.seriesmappings import addSeriesMapping
from app.db_models.tables.authors import doesAuthorExist
from app.db_models.tables.books import doesBookExist
from app.db_models.tables.genres import doesGenreExist
from app.db_models.tables.narrators import doesNarratorExist
from app.db_models.tables.series import doesSeriesExist
from app.db_models.tables.authors import getAuthor
from app.db_models.tables.genres import getGenre
from app.db_models.tables.narrators import getNarrator
from app.db_models.tables.series import getSeries


from app.app_helpers.audiobookshelf.audiobookshelf_api import (
    getLibraryItem,
    getLibraryItems,
)


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


# service: SQLiteService = Depends(get_db_service)


def refreshAbsData(engine, url, abs_api_key, library_id) -> None:
    abs_books = []
    abs_books = getLibraryItems(url, abs_api_key, library_id)

    for abs_book in abs_books["results"]:
        if not doesBookExist(engine, abs_book["id"]):
            book = Book()
            book = getLibraryItem(url, abs_api_key, abs_book["id"])

            if not doesBookExist(engine, book.bookAsin) and book.bookAsin is not None:
                db_book_id = addBook(engine, book)
            else:
                print(f"duplicate book or missing asin: {book.title} {book.bookAsin}")
                continue

            #### Authors
            authors = []
            authors = book.authors
            # for each author of the book
            if authors:
                for single_author in authors:
                    # check if the author already exists in the authors table
                    # if not add the author and get the new author id
                    if not doesAuthorExist(engine, single_author.name):
                        author_db_id = addAuthor(engine, single_author)
                    else:
                        author_db_id = getAuthor(engine, single_author.name).id

                    # link the author in the authors table to the entry in the authorsbooks table
                    addAuthorMapping(engine, author_db_id, db_book_id)

            #### Narrators
            narrators = []
            narrators = book.narrators
            # for each narrator of the book
            if narrators:
                for single_narrator in narrators:
                    # check if the narrator already exists in the narrators table
                    # if not add the narrator and get the new narrator id
                    if not doesNarratorExist(engine, single_narrator.name):
                        narrator_db_id = addNarrator(engine, single_narrator)
                    else:
                        narrator_db_id = getNarrator(engine, single_narrator.name).id

                    # link the narrator in the narrators table to the entry in the Narratorsbooks table
                    addNarratorMapping(engine, narrator_db_id, db_book_id)

            #### Series
            # for each narrator of the book
            series = []
            series = book.series
            if series:
                for single_series in series:
                    # check if the series already exists in the series table
                    # if not add the series and get the new series id
                    if not doesSeriesExist(engine, single_series.name):
                        series_db_id = addSeries(engine, single_series)
                    else:
                        series_db_id = getSeries(engine, single_series.name).id

                    # link the narrator in the narrators table to the entry in the Narratorsbooks table
                    addSeriesMapping(
                        engine, series_db_id, db_book_id, single_series.sequence
                    )

            #### Genres
            genres = []
            genres = book.genres
            # for each genre of the book
            if genres:
                for single_genre in genres:
                    # check if the genre already exists in the genres table
                    # if not add the genre and get the new genre id
                    if not doesGenreExist(engine, single_genre.name):
                        genre_db_id = addGenre(engine, single_genre)
                    else:
                        genre_db_id = getGenre(engine, single_genre.name).id

                    # link the genre in the genres table to the entry in the Genresbooks table
                    addGenreMapping(engine, genre_db_id, db_book_id)
