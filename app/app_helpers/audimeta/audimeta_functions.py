from fastapi import Depends
from app.app_helpers.audimeta import audimeta_api

from app.db_models.tables.authorsmappings import (
    addAuthorMapping,
    getAuthorMappingByBook,
)
from app.db_models.tables.books import addBook, getBook
from app.db_models.tables.series import (
    addSeries,
    updateSeries,
    getSeries,
    cleanupDanglingSeries,
    calculateSeriesRating,
    getAllSeries,
)
from app.db_models.tables.seriesmappings import addSeriesMapping, getSeriesMappingByBook
from app.db_models.tables.authors import (
    addAuthor,
    updateAuthor,
    getAuthor,
    cleanupDanglingAuthors,
)
from app.db_models.tables.genres import addGenre, updateGenre, getGenre
from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator
from app.db_models.tables.narratormappings import (
    addNarratorMapping,
    getNarratorMappingByBook,
)
from app.db_models.tables.genremappings import addGenreMapping, getGenreMappingByBook
from app.services.sqlite import SQLiteService

# setup global services
db_service = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


def getMissingBooks(service: SQLiteService) -> None:
    all_series = getAllSeries(service)

    for single_series in all_series:
        books_in_series = audimeta_api.getAudimetaSeriesOfBooksAsBooks(
            single_series.seriesAsin
        )

        for single_book in books_in_series:
            if not getBook(single_book.bookAsin, service):
                print("-----------------------------------")
                single_book.isOwned = False
                addBook(single_book, service)

                # series
                if len(single_book.series) > 0:
                    for single_series in single_book.series:
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
                        if not getSeriesMappingByBook(single_book.id, service):
                            addSeriesMapping(
                                single_series.id,
                                single_book.id,
                                single_series.sequence,
                                service,
                            )

                # authors
                if len(single_book.authors) > 0:
                    for single_authors in single_book.authors:
                        if getAuthor(single_authors.name, service):
                            library_authors = getAuthor(single_authors.name, service)
                            single_authors.id = library_authors.id
                            updateAuthor(single_authors, service)
                        else:
                            single_authors.id = addAuthor(single_authors, service)
                            addAuthorMapping(single_authors.id, single_book.id, service)

                        if not getAuthorMappingByBook(single_book.id, service):
                            addAuthorMapping(single_authors.id, single_book.id, service)

                # narrators
                if len(single_book.narrators) > 0:
                    for single_narrators in single_book.narrators:
                        if getNarrator(single_narrators.name, service):
                            library_narrators = getNarrator(
                                single_narrators.name, service
                            )
                            single_narrators.id = library_narrators.id
                            updateNarrator(single_narrators, service)
                        else:
                            single_narrators.id = addNarrator(single_narrators, service)

                        if not getNarratorMappingByBook(single_book.id, service):
                            addNarratorMapping(
                                single_narrators.id, single_book.id, service
                            )

                # genres
                if len(single_book.genres) > 0:
                    for single_genres in single_book.genres:
                        if getGenre(single_genres.name, service):
                            library_genres = getGenre(single_genres.name, service)
                            single_genres.id = library_genres.id
                            updateGenre(single_genres, service)
                        else:
                            single_genres.id = addGenre(single_genres, service)
                        if not getGenreMappingByBook(single_book.id, service):
                            addGenreMapping(single_genres.id, single_book.id, service)

    cleanupDanglingSeries(service)
    cleanupDanglingAuthors(service)
