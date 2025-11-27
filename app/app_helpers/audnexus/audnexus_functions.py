from app.app_helpers.audnexus import audnexus_api

from app.db_models.tables.books import updateBook, getAllBooks, getBook
from app.db_models.tables.series import addSeries, updateSeries, getSeries, cleanupDanglingSeries
from app.db_models.tables.seriesmappings import addSeriesMapping
from app.db_models.tables.authors import updateAuthor, getAuthor
from app.db_models.tables.genres import updateGenre, getGenre
from app.db_models.tables.narrators import updateNarrator, getNarrator


def backfillAudnexusBookData(engine) -> None:
    """
    Populates missing book, author, genre, narrator, and series information from audimeta.
    """

    all_books = getAllBooks(engine)

    for single_book in all_books:
        audnexus_book = audnexus_api.getAudnexusBookAsBook(single_book.bookAsin)

        if audnexus_book is None:
            continue  # Skip this book
        
        library_book = getBook(engine, audnexus_book.bookAsin)
        audnexus_book.id = library_book.id
        audnexus_book.isOwned = library_book.isOwned
        updateBook(engine, audnexus_book)

        if len(audnexus_book.series) > 0:
            for single_series in audnexus_book.series:
                if getSeries(engine, single_series.name):
                    library_series = getSeries(engine, single_series.name)
                    single_series.id = library_series.id
                    updateSeries(engine, single_series)
                else:
                    db_id = addSeries(engine, single_series)
                    addSeriesMapping(engine, db_id, audnexus_book.id, single_series.sequence)


    cleanupDanglingSeries(engine)