import audible
from fastapi import Depends
from app.app_helpers.audibleapi import (
    audibleapi_helpers as audible_helpers,
)  # returnListofBookObjs, returnBookObj
from app.app_helpers.audibleapi.audibleapi_api import (
    getAudibleBooksInSeries,
    getAudibleBook,
)

from app.custom_objects import book
from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series
from app.services.sqlite import SQLiteService

from app.db_models.tables.authors import (
    addAuthor,
    updateAuthor,
    getAuthor,
    doesAuthorExist,
)
from app.db_models.tables.authorsmappings import (
    addAuthorMapping,
    getAuthorMappingByBook,
)
from app.db_models.tables.books import (
    addBook,
    returnBookObj,
    updateBook,
    getBook,
    doesBookExist,
    getAllBooks,
)
from app.db_models.tables.genres import addGenre, updateGenre, getGenre, doesGenreExist
from app.db_models.tables.genremappings import addGenreMapping, getGenreMappingByBook
from app.db_models.tables.narrators import (
    addNarrator,
    updateNarrator,
    getNarrator,
    doesNarratorExist,
)
from app.db_models.tables.narratormappings import (
    addNarratorMapping,
    getNarratorMappingByBook,
)
from app.db_models.tables.series import (
    addSeries,
    updateSeries,
    getSeries,
    doesSeriesExist,
    getAllSeries,
    getSeriesByBook,
    calculateSeriesRating,
)
from app.db_models.tables.seriesmappings import (
    addSeriesMapping,
    getSeriesMappingByBook,
    getSeriesMappingBySeries,
)


# from app.db_models.tables.authorsmappings import addAuthorMapping, getAuthorMappingByBook
# from app.db_models.tables.books import addBook, getBook
# from app.db_models.tables.series import addSeries, updateSeries, getSeries, cleanupDanglingSeries, calculateSeriesRating, getAllSeries
# from app.db_models.tables.seriesmappings import addSeriesMapping, getSeriesMappingByBook, getSeriesMappingBySeries
# from app.db_models.tables.authors import addAuthor, updateAuthor, getAuthor, cleanupDanglingAuthors
# from app.db_models.tables.genres import addGenre, updateGenre, getGenre
# from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator
# from app.db_models.tables.narratormappings import addNarratorMapping, getNarratorMappingByBook
# from app.db_models.tables.genremappings import addGenreMapping, getGenreMappingByBook


def getMissingBooks(auth, service: SQLiteService = Depends(get_db_service)):
    """
    Populates missing book, author, genre, narrator, and series information from audible.
    """

    # get list of book asins in library, one per series
    all_series = getAllSeries(service)
    library_book_asins = []
    for item in all_series:
        series_id = item.id
        book_id = getSeriesMappingBySeries(series_id, service)[0].bookId
        library_book = getBook(book_id, service)
        library_book_asins.append(library_book.bookAsin)

    # get list of audible books
    audible_books = []
    for library_book_asin in library_book_asins:
        audible_books_in_series = []
        audible_books_in_series = getAudibleBooksInSeries(auth, library_book_asin)

        for book_in_series in audible_books_in_series:
            audible_books.append(book_in_series)

    for single_book in audible_books:
        if not getBook(single_book.bookAsin, service):
            processBook(single_book, service)

    # cleanupDanglingSeries(service)
    # cleanupDanglingAuthors(service)

    print("Audible backfill complete.")


# def backfillAudibleDataMissedBooks(engine, auth):
#     """Find books that are missing audible data and reprocess using getAudibleBook to lookup the books individually."""

#     # get all books in library
#     all_books = getAllBooks(engine)

#     # make a list of the books missing audible information
#     # missing imageUrl is a good indicator of this.
#     books_missing_info = []
#     for single_book in all_books:
#         if not single_book.imageUrl:
#             books_missing_info.append(single_book)

#     # try to lookup audible metadata for books missing information.
#     for single_book in books_missing_info:
#         book_to_process = getAudibleBook(auth, single_book.bookAsin)
#         book_obj = audible_helpers.returnBookObj(book_to_process, True)
#         processBook(engine, book_obj)


def processBook(single_book, service: SQLiteService = Depends(get_db_service)) -> None:
    """helper function for adding audible book metadata to the database"""
    print(f"---Processing {single_book.title}")
    # books
    if not doesBookExist(single_book.bookAsin, service):
        # add new DB entry
        single_book.isOwned = False
        single_book.id = addBook(single_book, service)
    else:
        # update metadata on existing db entry
        book = Book()
        book = getBook(single_book.bookAsin, service)
        single_book.id = book.id
        single_book.isOwned = book.isOwned
        single_book.id = updateBook(single_book, service)

    # authors
    for single_author in single_book.authors:
        if not doesAuthorExist(single_author.name, service):
            # add new DB entry
            single_author.id = addAuthor(single_author, service)
        else:
            # update metadata on existing db entry
            author = Author()
            author = getAuthor(single_author.name, service)
            single_author.id = author.id
            updateAuthor(single_author, service)
        if not getAuthorMappingByBook(single_book.id, service):
            addAuthorMapping(single_author.id, single_book.id, service)

    # narrators
    for single_narrator in single_book.narrators:
        if not doesNarratorExist(single_narrator.name, service):
            # add new DB entry
            single_narrator.id = addNarrator(single_narrator, service)
        else:
            # update metadata on existing db entry
            narrator = Narrator()
            narrator = getNarrator(single_narrator.name, service)
            single_narrator.id = narrator.id
            updateNarrator(single_narrator, service)
        if not getNarratorMappingByBook(single_book.id, service):
            addNarratorMapping(single_narrator.id, single_book.id, service)

    # series
    for single_series in single_book.series:
        if not doesSeriesExist(single_series.name, service):
            # add new DB entry
            single_series.id = addSeries(single_series, service)

            # calculate series rating
            single_series.rating = calculateSeriesRating(single_series.id, service)
            updateSeries(single_series, service)
        else:
            # update metadata on existing db entry
            series = Series()
            series = getSeries(single_series.name, service)
            single_series.id = series.id
            # calculate series rating
            single_series.rating = calculateSeriesRating(single_series.id, service)

            updateSeries(single_series, service)
        if not getSeriesMappingByBook(single_book.id, service):
            addSeriesMapping(
                single_series.id, single_book.id, single_series.sequence, service
            )

    # genres
    for single_genre in single_book.genres:
        if not doesGenreExist(single_genre.name, service):
            # add new DB entry
            single_genre.id = addGenre(single_genre, service)
        else:
            # update metadata on existing db entry
            genre = Genre()
            genre = getGenre(single_genre.name, service)
            single_genre.id = genre.id
            updateGenre(single_genre, service)
        if not getGenreMappingByBook(single_book.id, service):
            addGenreMapping(single_genre.id, single_book.id, service)
