from app.app_helpers.audibleapi.helpers import returnListofBookObjs
from app.app_helpers.audibleapi.api import getAudibleBooksInSeries

from app.custom_objects.author import Author
from app.custom_objects.book import Book
from app.custom_objects.genre import Genre
from app.custom_objects.narrator import Narrator
from app.custom_objects.series import Series

from app.db_models.tables.authors import addAuthor, updateAuthor, getAuthor, doesAuthorExist
from app.db_models.tables.authorsmappings import addAuthorMapping
from app.db_models.tables.books import addBook, updateBook, getBook, doesBookExist, getAllBooks
from app.db_models.tables.genres import addGenre, updateGenre, getGenre, doesGenreExist
from app.db_models.tables.genremappings import addGenreMapping
from app.db_models.tables.narrators import addNarrator, updateNarrator, getNarrator, doesNarratorExist
from app.db_models.tables.narratormappings import addNarratorMapping
from app.db_models.tables.series import addSeries, updateSeries, getSeries, doesSeriesExist
from app.db_models.tables.seriesmappings import addSeriesMapping



# probably will replace getMissingBooksFromSeries
def backfillAudibleData(engine, auth):
    """
    Populates missing book, author, genre, narrator, and series information from audible.
    """
    def logOut(object, adding: bool) -> None:
        # if adding is True:
        #     if type(object) is Book:
        #         print(f"Adding book:       {object.title} - {object.id}")
        #     if type(object) is Author:
        #         print(f"Adding author:     {object.name} - {object.id}")
        #     if type(object) is Series:
        #         print(f"Adding series:     {object.name} - {object.id}")
        #     if type(object) is Genre:
        #         print(f"Adding genre:      {object.name} - {object.id}")
        #     if type(object) is Narrator:
        #         print(f"Adding narrator:   {object.name} - {object.id}")
        # else:
        #     if type(object) is Book:
        #         print(f"Updating book:     {object.title} - {object.id}")
        #     if type(object) is Author:
        #         print(f"Updating author:   {object.name} - {object.id}")
        #     if type(object) is Series:
        #         print(f"Updating series:   {object.name} - {object.id}")
        #     if type(object) is Genre:
        #         print(f"Updating genre:    {object.name} - {object.id}")
        #     if type(object) is Narrator:
        #         print(f"Updating narrator: {object.name} - {object.id}")
        pass

    for item in getAllBooks(engine):
        books_in_series = returnListofBookObjs(getAudibleBooksInSeries(auth, item.bookAsin))

        for single_book in books_in_series:
            print(f"-----------Procesing: {single_book.title}")

            # books
            if not doesBookExist(engine, single_book.bookAsin) and not doesBookExist(engine, single_book.bookAsin):
                # add new DB entry
                single_book.isOwned = False
                single_book.id = addBook(engine, single_book)
                logOut(single_book, True)
            else:
                # update metadata on existing db entry
                book = Book()
                book = getBook(engine, single_book.bookAsin)
                single_book.id = book.id
                single_book.isOwned = book.isOwned
                updateBook(engine, single_book)
                logOut(single_book, False)

            # authors
            for single_author in single_book.authors:
                if not doesAuthorExist(engine, single_author.name):
                    # add new DB entry
                    new_author_id = addAuthor(engine, single_author)
                    addAuthorMapping(engine, new_author_id, single_book.id)
                    logOut(single_author, True)
                else:
                    # update metadata on existing db entry
                    author = Author()
                    author = getAuthor(engine, single_author.name)
                    single_author.id = author.id
                    updateAuthor(engine, single_author)
                    logOut(single_author, False)

            # narrators
            for single_narrator in single_book.narrators:
                if not doesNarratorExist(engine, single_narrator.name):
                    # add new DB entry
                    new_narrator_id = addNarrator(engine, single_narrator)
                    addNarratorMapping(engine, new_narrator_id, single_book.id)
                    logOut(single_author, True)
                else:
                    # update metadata on existing db entry
                    narrator = Narrator()
                    narrator = getNarrator(engine, single_narrator.name)
                    single_narrator.id = narrator.id
                    updateNarrator(engine, single_narrator)
                    logOut(single_author, False)

            # series
            for single_series in single_book.series:
                if not doesSeriesExist(engine, single_series.name):
                    # add new DB entry
                    single_series.totalBooksInSeries = len(books_in_series) # max returned by audible api is 50
                    new_series_id = addSeries(engine, single_series)
                    addSeriesMapping(engine, new_series_id, single_book.id, single_series.sequence)
                    logOut(single_series, True)
                else:
                    # update metadata on existing db entry
                    series = Series()
                    series = getSeries(engine, single_series.name)
                    single_series.id = series.id
                    single_series.totalBooksInSeries = len(books_in_series) # max returned by audible api is 50
                    updateSeries(engine, single_series)
                    logOut(single_series, False)

            # genre
            for single_genre in single_book.genres:
                if not doesGenreExist(engine, single_series.name):
                    # add new DB entry
                    new_genre_id = addGenre(engine, single_genre)
                    addGenreMapping(engine, new_genre_id, single_book.id)
                    logOut(single_genre, True)
                else:
                    # update metadata on existing db entry
                    genre = Series()
                    genre = getGenre(engine, single_genre.name)
                    single_genre.id = genre.id
                    updateGenre(engine, single_genre)
                    logOut(single_genre, False)
    print("Audible backfill complete.")