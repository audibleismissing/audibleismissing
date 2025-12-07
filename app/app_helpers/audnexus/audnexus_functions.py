from fastapi import Depends
from app.app_helpers.audnexus import audnexus_api

from app.db_models.tables.authorsmappings import addAuthorMapping
from app.db_models.tables.books import updateBook, getAllBooks, getBook
from app.db_models.tables.series import (
    addSeries,
    updateSeries,
    getSeries,
    cleanupDanglingSeries,
    calculateSeriesRating,
)
from app.db_models.tables.seriesmappings import addSeriesMapping
from app.db_models.tables.authors import (
    addAuthor,
    updateAuthor,
    getAuthor,
    cleanupDanglingAuthors,
)
from app.db_models.tables.genres import addGenre, updateGenre, getGenre
from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator
from app.db_models.tables.narratormappings import addNarratorMapping
from app.db_models.tables.genremappings import addGenreMapping
from app.services.sqlite import SQLiteService

# setup global services
db_service = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


def backfillAudnexusBookData(service: SQLiteService = Depends(get_db_service)) -> None:
    """
    Populates missing book, author, genre, narrator, and series information from audimeta.
    """

    all_books = getAllBooks(service)

    for single_book in all_books:
        print("-----------------------------------")
        audnexus_book = audnexus_api.getAudnexusBookAsBook(single_book.bookAsin)

        if audnexus_book is None:
            continue  # Skip this book

        library_book = getBook(audnexus_book.bookAsin, service)
        audnexus_book.id = library_book.id
        audnexus_book.isOwned = library_book.isOwned
        updateBook(audnexus_book, service)

        # series
        if len(audnexus_book.series) > 0:
            for single_series in audnexus_book.series:
                if getSeries(single_series.name, service):
                    library_series = getSeries(single_series.name, service)
                    single_series.id = library_series.id

                    # calculate series rating
                    single_series.rating = calculateSeriesRating(
                        single_series.id, service
                    )

                    updateSeries(single_series, service)
                else:
                    single_series.id = addSeries(single_series, service)

                    # calculate series rating
                    single_series.rating = calculateSeriesRating(
                        single_series.id, service
                    )

                    addSeriesMapping(
                        single_series.id,
                        audnexus_book.id,
                        single_series.sequence,
                        service,
                    )

        # authors
        if len(audnexus_book.authors) > 0:
            for single_authors in audnexus_book.authors:
                if getAuthor(single_authors.name, service):
                    library_authors = getAuthor(single_authors.name, service)
                    single_authors.id = library_authors.id
                    updateAuthor(single_authors, service)
                else:
                    single_authors.id = addAuthor(single_authors, service)
                    addAuthorMapping(single_authors.id, audnexus_book.id, service)

        # narrators
        if len(audnexus_book.narrators) > 0:
            for single_narrators in audnexus_book.narrators:
                if getNarrator(single_narrators.name, service):
                    library_narrators = getNarrator(single_narrators.name, service)
                    single_narrators.id = library_narrators.id
                    updateNarrator(single_narrators, service)
                else:
                    single_narrators.id = addNarrator(single_narrators, service)
                    addNarratorMapping(single_narrators.id, audnexus_book.id, service)

        # genres
        if len(audnexus_book.genres) > 0:
            for single_genres in audnexus_book.genres:
                if getGenre(single_genres.name, service):
                    library_genres = getGenre(single_genres.name, service)
                    single_genres.id = library_genres.id
                    updateGenre(single_genres, service)
                else:
                    single_genres.id = addGenre(single_genres, service)
                    addGenreMapping(single_genres.id, audnexus_book.id, service)

    cleanupDanglingSeries(service)
    cleanupDanglingAuthors(service)
