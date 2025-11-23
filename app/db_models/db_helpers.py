import sqlite3

from sqlmodel import SQLModel, create_engine

from app.app_helpers.audibleapi import auth
from app.db_models.views import booksandseries
from app.custom_objects import settings
from app.custom_objects.book import jsonToBook
from app.custom_objects.author import jsonToAuthor, Author
from app.custom_objects.series import jsonToSeries
from app.custom_objects.narrator import jsonToNarrator
from app.custom_objects.genre import jsonToGenre
from app.app_helpers.testdata.tools import importJson, exportJson
from app.db_models.tables.books import getAllBooks, addBook, doesBookExist
from app.db_models.tables.authors import addAuthor, doesAuthorExist, getAuthor, updateAuthor
from app.db_models.tables.authorsmappings import addAuthorMapping
from app.db_models.tables.genres import addGenre, doesGenreExist
from app.db_models.tables.genremappings import addGenreMapping
from app.db_models.tables.narrators import addNarrator, doesNarratorExist
from app.db_models.tables.narratormappings import addNarratorMapping
from app.db_models.tables.series import addSeries, doesSeriesExist
from app.db_models.tables.seriesmappings import addSeriesMapping



def connectToDb() -> create_engine:
    sqlite_path = (settings.readSettings('settings.toml')).sqlite_path

    sqlite_url = f"sqlite:///{sqlite_path}"
    return create_engine(sqlite_url, echo=False)


def createTables(engine, sqlite_db):
    SQLModel.metadata.create_all(engine)
    booksandseries.createBooksAndSeriesView(sqlite_db)


def dropAllTables(sqlite_db) -> None:
    try:
        with sqlite3.connect(sqlite_db) as connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS books")
            cursor.execute("DROP TABLE IF EXISTS series")
            cursor.execute("DROP TABLE IF EXISTS seriesmappings")
            cursor.execute("DROP TABLE IF EXISTS narrators")
            cursor.execute("DROP TABLE IF EXISTS narratormappings")
            cursor.execute("DROP TABLE IF EXISTS authors")
            cursor.execute("DROP TABLE IF EXISTS authormappings")
            cursor.execute("DROP TABLE IF EXISTS genres")
            cursor.execute("DROP TABLE IF EXISTS genremappings")
            cursor.execute("DROP VIEW IF EXISTS booksandseries")

            connection.commit()
    except sqlite3.Error as error:
        print('DB conneciton error occured -', error)


def resetAllData(engine, sqlite_db) -> None:
    print(f"Deleting tables: {sqlite_db}")
    dropAllTables(sqlite_db)

    print(f"Creating tables: {sqlite_db}")
    createTables(engine, sqlite_db)


def exportDb(engine) -> None:
    print("Exporting....")
    # books = getAllBooks(engine)
    # exportJson(Book.serialize(books), "app/app_helpers/testdata/testdata_large.json")

    # books_to_export = []
    # for single_book in books:
    #     for author in single_book.authors:
    #         if author.get('name') == "pirateaba":
    #             books_to_export.append(Book.toJson(single_book))
    # exportJson(books_to_export, "app/app_helpers/testdata/testdata_small.json")
                


def importDb(engine) -> None:
    print("Importing....")
    books = importJson("app/app_helpers/testdata/testdata_small.json")
    for single_book in books:
        if single_book['authors'][0]['name'] == "pirateaba" and not doesBookExist(engine, single_book['title']):
            book = jsonToBook(single_book)
            book_id = addBook(engine, book)
            for single_author in single_book['authors']:
                author = jsonToAuthor(single_author)
                if not doesAuthorExist(engine, author.name):
                    author_id = addAuthor(engine, author)
                addAuthorMapping(engine, author_id, book_id)
            for single_genre in single_book['genres']:
                genre = jsonToGenre(single_genre)
                if not doesGenreExist(engine, genre.name):
                    genre_id = addGenre(engine, genre)
                addGenreMapping(engine, genre_id, book_id)
            for single_narrator in single_book['narrators']:
                narrator = jsonToNarrator(single_narrator)
                if not doesNarratorExist(engine, narrator.name):
                    narrator_id = addNarrator(engine, narrator)
                addNarratorMapping(engine, narrator_id, book_id)
            for single_series in single_book['series']:
                series = jsonToSeries(single_series)
                if not doesSeriesExist(engine, series.name):
                    series_id = addSeries(engine, series)
                addSeriesMapping(engine, series_id, book_id, series.sequence)
    print("Completed import")
