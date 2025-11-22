import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select
from app.custom_objects.genre import Genre
from app.db_models.tables.genremappings import GenreMappingsTable


class GenresTable(SQLModel, table=True):
    __tablename__ = "genres"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str | None


def addGenre(engine:create_engine, genre:Genre) -> str:
    """Add genre to db"""
    # check if genre already exists
    if not doesGenreExist(engine, genre.name):
        row = GenresTable(
            name=genre.name,
        )

        with Session(engine) as session:
            session.add(row)
            session.commit()
            session.refresh(row)
            return row.id
    return None


def getGenre(engine:create_engine, search_string):
    """Get genre from db"""
    with Session(engine) as session:
        statement = select(GenresTable).where(or_(GenresTable.name == search_string, GenresTable.id == search_string))

        results = session.exec(statement).first()
        if results:
            return returnGenreObj(results)
        return None


def updateGenre(engine: create_engine, genre: Genre) -> None:
    """Update genre in db"""
    with Session(engine) as session:
        statement = select(GenresTable).where(GenresTable.id == genre.id)
        results = session.exec(statement).one()

        results.name = genre.name

        session.add(results)
        session.commit()


def deleteGenre():
    """Delete genre from db"""


def doesGenreExist(engine:create_engine, search_string) -> bool:
    with Session(engine) as session:
        statement = select(GenresTable).where(or_(GenresTable.name == search_string, GenresTable.id == search_string))

        results = session.exec(statement)
        if len(results.all()) > 0:
            return True
        else:
            return False


def getBookGenres(engine:create_engine, book_id) -> list:
    """Get genres by book id"""
    with Session(engine) as session:
        # get the authors related to a specific book id
        genre_mappings_query = select(GenreMappingsTable).where(GenreMappingsTable.bookId == book_id)
        genre_mappings_table = session.exec(genre_mappings_query).all()

        genres = []
        for genre_mappings_row in genre_mappings_table:
            genre_query = select(GenresTable).where(GenresTable.id == genre_mappings_row.genreId)
            genres_table = session.exec(genre_query).one_or_none()

            genre = Genre()
            genre.id = genres_table.id
            genre.name = genres_table.name
            genres.append(genre)

        return genres
    


def returnGenreObj(sql_data) -> Genre:
    genre = Genre()
    genre.id = sql_data.id
    genre.name = sql_data.name
    return genre