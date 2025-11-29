import json
import sqlite3

from sqlmodel import Session, SQLModel, create_engine, select

from app.custom_objects import settings
from app.custom_objects.settings import readSettings
from app.db_models.tables.authors import AuthorsTable
from app.db_models.tables.authorsmappings import AuthorsMappingsTable
from app.db_models.tables.books import BooksTable
from app.db_models.tables.bookwishlist import BookWishListTable
from app.db_models.tables.genremappings import GenreMappingsTable
from app.db_models.tables.genres import GenresTable
from app.db_models.tables.narratormappings import NarratorMappingsTable
from app.db_models.tables.narrators import NarratorsTable
from app.db_models.tables.series import SeriesTable
from app.db_models.tables.seriesmappings import SeriesMappingsTable
from app.db_models.tables.serieswatchlist import SeriesWatchListTable
from app.db_models.views import booksandseries, seriesandcounts

json_file = "/config/db_dump.json"

config = readSettings()


def connectToDb() -> create_engine:
    sqlite_path = (settings.readSettings()).sqlite_path

    sqlite_url = f"sqlite:///{sqlite_path}"
    return create_engine(sqlite_url, echo=False)


def createTables(engine, sqlite_db):
    SQLModel.metadata.create_all(engine)
    booksandseries.createBooksAndSeriesView(sqlite_db)
    seriesandcounts.createSeriesAndCountsView(sqlite_db)


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
            cursor.execute("DROP TABLE IF EXISTS serieswatchlist")
            cursor.execute("DROP TABLE IF EXISTS bookwishlist")
            cursor.execute("DROP VIEW IF EXISTS booksandseries")
            cursor.execute("DROP VIEW IF EXISTS seriesandcounts")

            connection.commit()
    except sqlite3.Error as error:
        print("DB conneciton error occured -", error)


def resetAllData(engine, sqlite_db) -> None:
    print(f"Deleting tables: {sqlite_db}")
    dropAllTables(sqlite_db)

    print(f"Creating tables: {sqlite_db}")
    createTables(engine, sqlite_db)


def exportDbToJson(engine):
    """Export all database tables to a JSON file."""
    data = {}

    with Session(engine) as session:
        # Export main tables
        data["authors"] = [
            row.model_dump() for row in session.exec(select(AuthorsTable)).all()
        ]
        data["books"] = [
            row.model_dump() for row in session.exec(select(BooksTable)).all()
        ]
        data["genres"] = [
            row.model_dump() for row in session.exec(select(GenresTable)).all()
        ]
        data["narrators"] = [
            row.model_dump() for row in session.exec(select(NarratorsTable)).all()
        ]
        data["series"] = [
            row.model_dump() for row in session.exec(select(SeriesTable)).all()
        ]

        # Export mapping tables
        data["authormappings"] = [
            row.model_dump() for row in session.exec(select(AuthorsMappingsTable)).all()
        ]
        data["genremappings"] = [
            row.model_dump() for row in session.exec(select(GenreMappingsTable)).all()
        ]
        data["narratormappings"] = [
            row.model_dump()
            for row in session.exec(select(NarratorMappingsTable)).all()
        ]
        data["seriesmappings"] = [
            row.model_dump() for row in session.exec(select(SeriesMappingsTable)).all()
        ]

        # Export wishlist tables
        data["bookwishlist"] = [
            row.model_dump() for row in session.exec(select(BookWishListTable)).all()
        ]
        data["serieswatchlist"] = [
            row.model_dump() for row in session.exec(select(SeriesWatchListTable)).all()
        ]

    with open(json_file, "w") as f:
        json.dump(
            data, f, indent=2, default=str
        )  # default=str to handle Decimal and datetime


def importJsonToDb(engine):
    """Import JSON data from file into the database, replacing existing data."""
    with open(json_file, "r") as f:
        data = json.load(f)

    with Session(engine) as session:
        resetAllData(engine, config.sqlite_path)

        # Insert main tables first
        for author_data in data.get("authors", []):
            author = AuthorsTable(**author_data)
            session.add(author)

        for book_data in data.get("books", []):
            book = BooksTable(**book_data)
            session.add(book)

        for genre_data in data.get("genres", []):
            genre = GenresTable(**genre_data)
            session.add(genre)

        for narrator_data in data.get("narrators", []):
            narrator = NarratorsTable(**narrator_data)
            session.add(narrator)

        for series_data in data.get("series", []):
            series = SeriesTable(**series_data)
            session.add(series)

        session.commit()  # Commit main tables

        # Insert mapping tables
        for mapping_data in data.get("authormappings", []):
            mapping = AuthorsMappingsTable(**mapping_data)
            session.add(mapping)

        for mapping_data in data.get("genremappings", []):
            mapping = GenreMappingsTable(**mapping_data)
            session.add(mapping)

        for mapping_data in data.get("narratormappings", []):
            mapping = NarratorMappingsTable(**mapping_data)
            session.add(mapping)

        for mapping_data in data.get("seriesmappings", []):
            mapping = SeriesMappingsTable(**mapping_data)
            session.add(mapping)

        # Insert wishlist tables
        for item_data in data.get("bookwishlist", []):
            item = BookWishListTable(**item_data)
            session.add(item)

        for item_data in data.get("serieswatchlist", []):
            item = SeriesWatchListTable(**item_data)
            session.add(item)

        session.commit()
