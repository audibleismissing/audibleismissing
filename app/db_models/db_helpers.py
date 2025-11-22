import sqlite3

from sqlmodel import SQLModel, create_engine

from app.db_models.views import booksandseries
from app.custom_objects import settings


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