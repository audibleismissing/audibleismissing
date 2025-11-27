from app.app_helpers.audimeta import audimeta_api

from app.db_models.tables.authorsmappings import addAuthorMapping, getAuthorMappingByBook
from app.db_models.tables.books import addBook, getBook
from app.db_models.tables.series import addSeries, updateSeries, getSeries, cleanupDanglingSeries, calculateSeriesRating, getAllSeries
from app.db_models.tables.seriesmappings import addSeriesMapping, getSeriesMappingByBook
from app.db_models.tables.authors import addAuthor, updateAuthor, getAuthor, cleanupDanglingAuthors
from app.db_models.tables.genres import addGenre, updateGenre, getGenre
from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator
from app.db_models.tables.narratormappings import addNarratorMapping, getNarratorMappingByBook
from app.db_models.tables.genremappings import addGenreMapping, getGenreMappingByBook



def getMissingBooks(engine) -> None:

    all_series = getAllSeries(engine)

    for single_series in all_series:
        books_in_series = audimeta_api.getAudimetaSeriesOfBooksAsBooks(single_series.seriesAsin)

        for single_book in books_in_series:
            if not getBook(engine, single_book.bookAsin):
                print("-----------------------------------")
                single_book.isOwned = False
                addBook(engine, single_book)

                # series
                if len(single_book.series) > 0:
                    for single_series in single_book.series:
                        if getSeries(engine, single_series.name):
                            library_series = getSeries(engine, single_series.name)
                            single_series.id = library_series.id

                            # calculate series rating
                            single_series.rating = calculateSeriesRating(engine, single_series.id)

                            updateSeries(engine, single_series)
                        else:
                            single_series.id = addSeries(engine, single_series)

                            # calculate series rating
                            single_series.rating = calculateSeriesRating(engine, single_series.id)
                        if not getSeriesMappingByBook(engine, single_book.id):
                            addSeriesMapping(engine, single_series.id, single_book.id, single_series.sequence)

                # authors
                if len(single_book.authors) > 0:
                    for single_authors in single_book.authors:
                        if getAuthor(engine, single_authors.name):
                            library_authors = getAuthor(engine, single_authors.name)
                            single_authors.id = library_authors.id
                            updateAuthor(engine, single_authors)
                        else:
                            single_authors.id = addAuthor(engine, single_authors)
                            addAuthorMapping(engine, single_authors.id, single_book.id)

                        if not getAuthorMappingByBook(engine, single_book.id):
                            addAuthorMapping(engine, single_authors.id, single_book.id)

                # narrators
                if len(single_book.narrators) > 0:
                    for single_narrators in single_book.narrators:
                        if getNarrator(engine, single_narrators.name):
                            library_narrators = getNarrator(engine, single_narrators.name)
                            single_narrators.id = library_narrators.id
                            updateNarrator(engine, single_narrators)
                        else:
                            single_narrators.id = addNarrator(engine, single_narrators)

                        if not getNarratorMappingByBook(engine, single_book.id):
                            addNarratorMapping(engine, single_narrators.id, single_book.id)
                            
                # genres
                if len(single_book.genres) > 0:
                    for single_genres in single_book.genres:
                        if getGenre(engine, single_genres.name):
                            library_genres = getGenre(engine, single_genres.name)
                            single_genres.id = library_genres.id
                            updateGenre(engine, single_genres)
                        else:
                            single_genres.id = addGenre(engine, single_genres)
                        if not getGenreMappingByBook(engine, single_book.id):
                            addGenreMapping(engine, single_genres.id, single_book.id)

    cleanupDanglingSeries(engine)
    cleanupDanglingAuthors(engine)
