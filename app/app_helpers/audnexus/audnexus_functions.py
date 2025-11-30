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


def backfillAudnexusBookData(engine) -> None:
    """
    Populates missing book, author, genre, narrator, and series information from audimeta.
    """

    all_books = getAllBooks(engine)

    for single_book in all_books:
        print("-----------------------------------")
        audnexus_book = audnexus_api.getAudnexusBookAsBook(single_book.bookAsin)

        if audnexus_book is None:
            continue  # Skip this book

        library_book = getBook(engine, audnexus_book.bookAsin)
        audnexus_book.id = library_book.id
        audnexus_book.isOwned = library_book.isOwned
        updateBook(engine, audnexus_book)

        # series
        if len(audnexus_book.series) > 0:
            for single_series in audnexus_book.series:
                if getSeries(engine, single_series.name):
                    library_series = getSeries(engine, single_series.name)
                    single_series.id = library_series.id

                    # calculate series rating
                    single_series.rating = calculateSeriesRating(
                        engine, single_series.id
                    )

                    updateSeries(engine, single_series)
                else:
                    single_series.id = addSeries(engine, single_series)

                    # calculate series rating
                    single_series.rating = calculateSeriesRating(
                        engine, single_series.id
                    )

                    addSeriesMapping(
                        engine,
                        single_series.id,
                        audnexus_book.id,
                        single_series.sequence,
                    )

        # authors
        if len(audnexus_book.authors) > 0:
            for single_authors in audnexus_book.authors:
                if getAuthor(engine, single_authors.name):
                    library_authors = getAuthor(engine, single_authors.name)
                    single_authors.id = library_authors.id
                    updateAuthor(engine, single_authors)
                else:
                    single_authors.id = addAuthor(engine, single_authors)
                    addAuthorMapping(engine, single_authors.id, audnexus_book.id)

        # narrators
        if len(audnexus_book.narrators) > 0:
            for single_narrators in audnexus_book.narrators:
                if getNarrator(engine, single_narrators.name):
                    library_narrators = getNarrator(engine, single_narrators.name)
                    single_narrators.id = library_narrators.id
                    updateNarrator(engine, single_narrators)
                else:
                    single_narrators.id = addNarrator(engine, single_narrators)
                    addNarratorMapping(engine, single_narrators.id, audnexus_book.id)

        # genres
        if len(audnexus_book.genres) > 0:
            for single_genres in audnexus_book.genres:
                if getGenre(engine, single_genres.name):
                    library_genres = getGenre(engine, single_genres.name)
                    single_genres.id = library_genres.id
                    updateGenre(engine, single_genres)
                else:
                    single_genres.id = addGenre(engine, single_genres)
                    addGenreMapping(engine, single_genres.id, audnexus_book.id)

    cleanupDanglingSeries(engine)
    cleanupDanglingAuthors(engine)
