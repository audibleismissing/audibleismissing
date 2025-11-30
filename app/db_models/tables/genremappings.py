import uuid

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select


class GenreMappingsTable(SQLModel, table=True):
    __tablename__ = "genremappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    genreId: str | None = Field(default=None, foreign_key="genres.id")
    bookId: str | None = Field(default=None, foreign_key="books.id")


def addGenreMapping(engine: create_engine, genre_id, book_id) -> str:
    """Add genre mapping to db"""
    print(f"Adding genre mapping: {genre_id} -> {book_id}")
    row = GenreMappingsTable(
        genreId=genre_id,
        bookId=book_id,
    )

    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getGenreMappingByBook(engine: create_engine, book_id):
    """Get genre mapping from db"""
    with Session(engine) as session:
        statement = select(GenreMappingsTable).where(
            GenreMappingsTable.bookId == book_id
        )

        results = session.exec(statement).first()
        if results:
            return results
        return None


def updateGenreMapping():
    """Update genre mapping in db"""


def deleteGenreMapping():
    """Delete genre mapping from db"""
