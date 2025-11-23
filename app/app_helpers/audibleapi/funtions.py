import audible
from app.app_helpers.audibleapi.helpers import returnListofBookObjs
from app.app_helpers.audibleapi.api import getAudibleBooksInSeries

from app.custom_objects import book
from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series

from app.db_models.tables.authors import addAuthor, updateAuthor, getAuthor, doesAuthorExist
from app.db_models.tables.authorsmappings import addAuthorMapping, getAuthorMappingByBook
from app.db_models.tables.books import addBook, updateBook, getBook, doesBookExist, getAllBooks
from app.db_models.tables.genres import addGenre, updateGenre, getGenre, doesGenreExist
from app.db_models.tables.genremappings import addGenreMapping, getGenreMappingByBook
from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator, doesNarratorExist
from app.db_models.tables.narratormappings import addNarratorMapping, getNarratorMappingByBook
from app.db_models.tables.series import addSeries, updateSeries, getSeries, doesSeriesExist, getAllSeries
from app.db_models.tables.seriesmappings import addSeriesMapping, getSeriesMappingByBook, getSeriesMappingBySeries



# probably will replace getMissingBooksFromSeries
def backfillAudibleData(engine, auth):
    """
    Populates missing book, author, genre, narrator, and series information from audible.
    """

    # get list of book asins in library, one per series
    all_series = getAllSeries(engine)
    library_book_asins = []
    for item in all_series:
        series_id = item.id
        book_id = getSeriesMappingBySeries(engine, series_id)[0].bookId
        library_book = getBook(engine, book_id)
        library_book_asins.append(library_book.bookAsin)
    
    # get list of audible books
    audible_books = []
    for library_book_asin in library_book_asins:
        books_in_series = []
        books_in_series = returnListofBookObjs(getAudibleBooksInSeries(auth, library_book_asin))
        for book_in_series in books_in_series:
            audible_books.append(book_in_series)

    for single_book in audible_books:
        # books
        if not doesBookExist(engine, single_book.bookAsin):
            # add new DB entry
            single_book.isOwned = False
            single_book.id = addBook(engine, single_book)
        else:
            # update metadata on existing db entry
            book = Book()
            book = getBook(engine, single_book.bookAsin)
            single_book.id = book.id
            single_book.isOwned = book.isOwned
            single_book.id = updateBook(engine, single_book)

        # authors
        for single_author in single_book.authors:
            if not doesAuthorExist(engine, single_author.name):
                # add new DB entry
                single_author.id = addAuthor(engine, single_author)
            else:
                # update metadata on existing db entry
                author = Author()
                author = getAuthor(engine, single_author.name)
                single_author.id = author.id
                updateAuthor(engine, single_author)
            if not getAuthorMappingByBook(engine, single_book.id):
                addAuthorMapping(engine, single_author.id, single_book.id)

        # narrators
        for single_narrator in single_book.narrators:
            if not doesNarratorExist(engine, single_narrator.name):
                # add new DB entry
                single_narrator.id = addNarrator(engine, single_narrator)
            else:
                # update metadata on existing db entry
                narrator = Narrator()
                narrator = getNarrator(engine, single_narrator.name)
                single_narrator.id = narrator.id
                updateNarrator(engine, single_narrator)
            if not getNarratorMappingByBook(engine, single_book.id):
                addNarratorMapping(engine, single_narrator.id, single_book.id)

        # series
        for single_series in single_book.series:
            if not doesSeriesExist(engine, single_series.name):
                # add new DB entry
                single_series.totalBooksInSeries = len(books_in_series) # max returned by audible api is 50
                single_series.id = addSeries(engine, single_series)
            else:
                # update metadata on existing db entry
                series = Series()
                series = getSeries(engine, single_series.name)
                single_series.id = series.id
                single_series.totalBooksInSeries = len(books_in_series) # max returned by audible api is 50
                updateSeries(engine, single_series)
            if not getSeriesMappingByBook(engine, single_book.id):
                addSeriesMapping(engine, single_series.id, single_book.id, single_series.sequence)

        # genre FIXME: genres mappings are being duplicated?
        for single_genre in single_book.genres:
            if not doesGenreExist(engine, single_genre.name):
                # add new DB entry
                single_genre.id = addGenre(engine, single_genre)
            else:
                # update metadata on existing db entry
                genre = Genre()
                genre = getGenre(engine, single_genre.name)
                single_genre.id = genre.id
                updateGenre(engine, single_genre)
            if not getGenreMappingByBook(engine, single_book.id):
                addGenreMapping(engine, single_genre.id, single_book.id)

    print("Audible backfill complete.")
