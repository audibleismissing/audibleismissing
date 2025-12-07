from re import S
import uuid
from fastapi import Depends

from sqlmodel import Field, SQLModel, Session, create_engine, or_, select
from app.services.sqlite import SQLiteService

# setup global services
db_service = None

def get_db_service() -> SQLiteService:
    """Get the database service instance."""
    global db_service
    if db_service is None:
        db_service = SQLiteService()
    return db_service


class SeriesMappingsTable(SQLModel, table=True):
    __tablename__ = "seriesmappings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sequence: str | None = None
    seriesId: str | None = Field(default=None, foreign_key="series.id")
    bookId: str | None = Field(default=None, foreign_key="books.id")


def addSeriesMapping(series_id, book_id, sequence, service: SQLiteService) -> str:
    """Add series mapping to db"""
    print(f"Adding series mapping: {series_id} -> {book_id}")
    row = SeriesMappingsTable(seriesId=series_id, bookId=book_id, sequence=sequence)

    with Session(service.engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row.id
    return None


def getSeriesMappingByBook(book_id, service: SQLiteService):
    """Get book id from series mapping from db by series id"""
    with Session(service.engine) as session:
        statement = select(SeriesMappingsTable).where(
            SeriesMappingsTable.bookId == book_id
        )

        results = session.exec(statement).first()
        if results:
            return results
        return None


def getSeriesMappingBySeries(series_id, service: SQLiteService):
    """Get book id from series mapping from db by series id"""
    with Session(service.engine) as session:
        statement = select(SeriesMappingsTable).where(
            SeriesMappingsTable.seriesId == series_id
        )

        results = session.exec(statement).all()
        if results:
            return results
        return None


def updateSeriesMapping():
    """Update series mapping in db"""


def deleteSeriesMapping(series_id, service: SQLiteService):
    """Delete series mapping from db"""
    print(f"Deleting series mapping: {series_id}")
    with Session(service.engine) as session:
        statement = select(SeriesMappingsTable).where(
            SeriesMappingsTable.seriesId == series_id
        )
        results = session.exec(statement)
        rows = results.all()
        for row in rows:
            session.delete(row)
