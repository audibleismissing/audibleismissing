from fastapi import Depends

from app.custom_objects.book import Book
from app.custom_objects.narrator import Narrator
from app.custom_objects.genre import Genre
from app.custom_objects.series import Series
from app.custom_objects.author import Author

from app.services.sqlite import SQLiteService

# setup global services
db_service = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


def returnBookObj(book_table, service: SQLiteService) -> Book:
    """Convert a BooksTable object to a Book object"""
    from app.db_models.tables.authors import getBookAuthors
    from app.db_models.tables.genres import getBookGenres
    from app.db_models.tables.narrators import getBookNarrators
    from app.db_models.tables.series import getBookSeries

    book = Book()

    # Map the fields from BooksTable to Book
    book.id = book_table.id
    book.title = book_table.title
    book.subtitle = book_table.subtitle
    book.publisher = book_table.publisher
    book.copyright = book_table.copyright
    book.description = book_table.description
    book.summary = book_table.summary
    book.isbn = book_table.isbn
    book.bookAsin = book_table.bookAsin
    book.region = book_table.region
    book.language = book_table.language
    book.isExplicit = book_table.isExplicit
    book.isAbridged = book_table.isAbridged
    book.releaseDate = book_table.releaseDate
    book.link = book_table.link
    book.imageUrl = book_table.imageUrl
    book.isOwned = book_table.isOwned
    book.audibleOverallAvgRating = book_table.audibleOverallAvgRating
    book.audiblePerformanceAvgRating = book_table.audiblePerformanceAvgRating
    book.audibleStoryAvgRating = book_table.audibleStoryAvgRating
    book.lengthMinutes = book_table.lengthMinutes
    book.isAudiobook = book_table.isAudiobook

    book.authors = getBookAuthors(book_table.id, service)
    book.genres = getBookGenres(book_table.id, service)
    book.series = getBookSeries(book_table.id, service)
    book.narrators = getBookNarrators(book_table.id, service)

    return book


def returnGenreObj(sql_data) -> Genre:
    genre = Genre()
    genre.id = sql_data.id
    genre.name = sql_data.name
    return genre


def returnSeriesObj(sql_data) -> Series:
    series = Series()
    series.id = sql_data.id
    series.name = sql_data.name
    series.seriesAsin = sql_data.seriesAsin
    if hasattr(sql_data, "sequence"):
        series.sequence = sql_data.sequence
    series.rating = sql_data.rating
    return series


def returnAuthorObj(sql_data) -> Author:
    author = Author()
    author.id = sql_data.id
    author.name = sql_data.name
    author.authorAsin = sql_data.authorAsin
    return author


def returnNarratorObj(sql_data) -> Narrator:
    narrator = Narrator()
    narrator.id = sql_data.id
    narrator.name = sql_data.name
    return narrator
