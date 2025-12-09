import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select
from app.custom_objects.genre import Genre
from app.db_models.tables.genremappings import GenreMappingsTable
from app.services.sqlite import SQLiteService
from app.db_models.tables.helpers import (
    returnAuthorObj,
    returnBookObj,
    returnGenreObj,
    returnNarratorObj,
    returnSeriesObj,
)

# setup global services
db_service = None


def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class GenresTable(SQLModel, table=True):
    __tablename__ = "genres"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str | None


def addGenre(genre: Genre, service: SQLiteService) -> str:
    """Add genre to db"""
    print(f"Adding genre: {genre.name}")
    row = GenresTable(
        name=genre.name,
    )

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id


def getGenre(search_string, service: SQLiteService):
    """Get genre from db"""
    with Session(service.engine) as session:
        statement = select(GenresTable).where(
            or_(GenresTable.name == search_string, GenresTable.id == search_string)
        )

        results = session.exec(statement).first()
        if results:
            return returnGenreObj(results)
        return None


def updateGenre(genre: Genre, service: SQLiteService) -> str:
    """Update genre in db"""
    print(f"Updating genre: {genre.name}")
    with Session(service.engine) as session:
        statement = select(GenresTable).where(GenresTable.id == genre.id)
        results = session.exec(statement).one()

        results.name = genre.name

        session.add(results)
        session.commit()
        return results.id


def deleteGenre():
    """Delete genre from db"""


def doesGenreExist(search_string, service: SQLiteService) -> bool:
    with Session(service.engine) as session:
        statement = select(GenresTable).where(
            or_(GenresTable.name == search_string, GenresTable.id == search_string)
        )

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getBookGenres(book_id, service: SQLiteService) -> list:
    """Get genres by book id"""
    with Session(service.engine) as session:
        # get the authors related to a specific book id
        genre_mappings_query = select(GenreMappingsTable).where(
            GenreMappingsTable.bookId == book_id
        )
        genre_mappings_table = session.exec(genre_mappings_query).all()

        genres = []
        for genre_mappings_row in genre_mappings_table:
            genre_query = select(GenresTable).where(
                GenresTable.id == genre_mappings_row.genreId
            )
            genres_table = session.exec(genre_query).one_or_none()

            genre = Genre()
            genre.id = genres_table.id
            genre.name = genres_table.name
            genres.append(genre)

        return genres
